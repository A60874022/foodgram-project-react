from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientAmount,
                            ListShopping, Recipe, Subscribe, Tag)


class IngredientInline(admin.StackedInline):
    model = Recipe.ingredients.through


class TagInline(admin.StackedInline):
    model = Recipe.tags.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time')
    search_fields = ('author', 'name', 'tags',)
    list_filter = ('author', 'name', )
    empty_value_display = '-пусто-'
    inlines = [IngredientInline, TagInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(ListShopping)
class ListShoppingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author')
    search_fields = ('author',)
    list_filter = ('author',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('following',)
    list_filter = ('following',)
