from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from user.models import User
from .fields import Base64ImageField
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 
        'last_name', 'is_subscribed', 'password')
        extra_kwargs = {'is_subscribed': {'required': False}}

class TagsSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")

class IndigrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indigrient
        fields = ('id', 'name', 'unit_of_measurement')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IndigrientSerializer(source="ingredient_to_recipe",
                                               many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart',  
                'name','image', 'text', 'cooking_time')
                
    def get_is_favorited(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and Favourites.objects.filter(recipe=recipe,
                                        user=current_user).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and Rurchases.objects.filter(recipe=recipe,
                                            user=current_user).exists()
        ):
            return True
        return False   

class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IndigrientSerializer(source="ingredient_to_recipe",
                                               many=True)
    tags = TagsSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    model = Recipe
    fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart',  
                'name','image', 'text', 'cooking_time')

    def get_is_favorited(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and Favourites.objects.filter(recipe=recipe,
                                        user=current_user).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and Rurchases.objects.filter(recipe=recipe,
                                            user=current_user).exists()
        ):
            return True
        return False  
    def create(self, validated_data):
        author = self.context["request"].user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredient_to_recipe")
        recipe = Recipe.objects.create(**validated_data, author=author)
        for tag in tags:
            recipe.tags.add(tag)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        if "ingredient_to_recipe" in validated_data:
            ingredients = validated_data.pop("ingredient_to_recipe")
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    unit_of_measurement = serializers.ReadOnlyField(
    source="ingredient.unit_of_measurement")

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'unit_of_measurement', 'quantity')


class FavouritesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')

class RurchasesSerializer(serializers.ModelSerializer):
    ingredient = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("ingredient",)

    def get_ingredient(self, recipe):
        ingredient = recipe.ingredients.all()
        return IndigrientSerializer(ingredient, many=True).data

class RecipeInfodSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    class Meta:
        model = Follow
        fields = ('email','id', 'username',   'first_name', 'last_name', 'is_subscribed')

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeInfodSerializer(queryset, many=True)

