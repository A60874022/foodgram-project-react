from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)
from recipes.models import (Favorite, Follow, Ingredient, IngredientAmount,
                            ListShopping, Recipe, Tag)
from user.models import User

from .fields import Base64ImageField


class UserSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_subscribed': {'required': False}}

    def get_is_subscribed(self, obj):
        return Follow.user(author__username=obj.username).exists()

class UserCreateSerializer(UserCreateSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')


class TagSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Ingredient."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        extra_kwargs = {'name': {'required': False},
                        'measurement_unit': {'required': False}}

class IngredientAmountSerializer(serializers.ModelSerializer):
    """Класс - сериализатор для модели IngredientAmount."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )
    
    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    """Класс - сериализатор модели Recipe."""
    tags = TagSerializer(read_only=False, many=True)
    author = UserSerializer(read_only=True, many=True)
    ingredients =  IngredientAmountSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None)

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
    ingredients = IngredientSerializer(source="ingredient_to_recipe",
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
        tags = validated_data.pop("tags")
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
        return IngredientSerializer(ingredients, many=True).data


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
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')


    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')[
                :recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeInfodSerializer(queryset, many=True).data
