from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from user.models import User

class IndigrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indigrient
        fields = ('id', 'name', 'unit_of_measurement')

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('author', 'name', 'image', 'text', 'indigrient', 'tags', 'cooking_time')

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    unit_of_measurement = serializers.ReadOnlyField(
    source="ingredient.unit_of_measurement")

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'unit_of_measurement', 'quantity')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'recipe', 'indigrient')

class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('id', 'name', 'image', 'cooking_time')

class RurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rurchases
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('email','id', 'username',   'first_name', 'last_name', 'is_subscribed')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','id', 'username', 'first_name', 'last_name', 'is_subscribed', 'password')