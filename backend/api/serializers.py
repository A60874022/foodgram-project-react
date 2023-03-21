from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Favorite, Follow, Indigrient, IngredientAmount,
                            ListShopping, Recipe, Tag)
from user.models import User

from .fields import Base64ImageField


class UserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()
    """Класс - сериализатор модели User."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')

    def get_is_subscribed(self, obj):
        return Follow.user(author__username=obj.username).exists()

class TagSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IndigrientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Indigrient."""
    class Meta:
        model = Indigrient
        fields = ('id', 'name', 'unit_of_measurement')
        extra_kwargs = {'name': {'required': False},
                        'unit_of_measurement': {'required': False}}


class RecipeSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Recipe."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IndigrientSerializer(source="ingredient_to_recipe",
                                      many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, recipe):
        """Функция для поля 'is_favorited'."""
        current_user = self.context["request"].user
        return Favorite.objects.filter(recipe=recipe,
                                       user=current_user).exists()

    def get_is_in_shopping_cart(self, recipe):
        """Функция для поля 'get_is_in_shopping_cart'."""
        current_user = self.context["request"].user
        return ListShopping.objects.filter(recipe=recipe,
                                           user=current_user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Класс - сериализатор для модели Recipe.
    Методы ["POST", "PATCH"]"""
    ingredients = IndigrientSerializer(source="ingredient_to_recipe",
                                      many=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        """Функция для поля 'is_favorited'."""
        current_user = self.context["request"].user
        return Favorite.objects.filter(recipe=recipe,
                                       user=current_user).exists()

    def get_is_in_shopping_cart(self, recipe):
        """Функция для поля 'get_is_in_shopping_cart'."""
        current_user = self.context["request"].user
        return ListShopping.objects.filter(recipe=recipe,
                                           user=current_user).exists()

    def create(self, validated_data):
        """Переобпределение метода create."""
        author = self.context["request"].user
        tags = validated_data.pop("tagы")
        ingredients = validated_data.pop("ingredients_to_recipe")
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.update(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        """Переобпределение метода update."""
        if "ingredient_to_recipe" in validated_data:
            ingredients = validated_data.pop("ingredient_to_recipe")
            recipe.ingredients.clear()
            self.create_ingredient(ingredients, recipe)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            recipe.tags.update(tags_data)
        return super().update(recipe, validated_data)


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели IngredientAmount."""
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    unit_of_measurement = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'unit_of_measurement', 'quantity')


class FavoriteSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели Favorite."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class ListShoppingSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели ListShopping."""
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("ingredients",)

    def get_ingredients(self, recipe):
        """Функция для поля 'ingredients'."""
        ingredients = recipe.ingredients.all()
        return IndigrientSerializer(ingredients, many=True).data


class RecipeInfodSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели Follow
    при GET запросе"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class FollowSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели Follow."""
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeInfodSerializer(queryset, many=True)
    

    def validate(self, data):
        author_id = self.context.get(
            'request').parser_context.get('kwargs').get('id')
        author = get_object_or_404(User, id=author_id)
        user = self.context.get('request').user
        if user.follower.filter(author=author_id).exists():
            raise ValidationError(
                detail='Подписка уже существует',
            )
        if user == author:
            raise ValidationError(
                detail='Нельзя подписаться на самого себя',
            )
        return data
