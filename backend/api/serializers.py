from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

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
        if self.context['request'].user.is_authenticated:
            user = get_object_or_404(
                User, username=self.context['request'].user)
            return user.follower.filter(author=obj.id).exists()
        return False


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
    tag = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredient = IndigrientSerializer(source="ingredient_to_recipe",
                                      many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'ingredient',
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
    ingredient = IndigrientSerializer(source="ingredient_to_recipe",
                                      many=True)
    tag = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'ingredient', 'is_favorited',
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
        tag = validated_data.pop("tag")
        ingredient = validated_data.pop("ingredient_to_recipe")
        recipe = Recipe.objects.create(**validated_data, author=author)
        for tag in Tag:
            recipe.Tag.add(tag)
        self.create_ingredient(ingredient, recipe)
        return recipe

    def update(self, recipe, validated_data):
        """Переобпределение метода update."""
        if "ingredient_to_recipe" in validated_data:
            ingredient = validated_data.pop("ingredient_to_recipe")
            recipe.ingredient.clear()
            self.create_ingredient(ingredient, recipe)
        if "tag" in validated_data:
            tag_data = validated_data.pop("tag")
            recipe.tag.set(tag_data)
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
    ingredient = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("ingredient",)

    def get_ingredient(self, recipe):
        """Функция для поля 'ingredient'."""
        ingredient = recipe.ingredient.all()
        return IndigrientSerializer(ingredient, many=True).data


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
