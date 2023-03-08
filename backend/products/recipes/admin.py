from django.contrib import admin
from recipes.models import (Favourites, Follow, Indigrient, IngredientAmount,
                            Recipe, Rurchases, Tags)


@admin.register(Indigrient)
class IndigrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',
                    'amount_tags', 'amount_ingredients')
    search_fields = ('author', 'name', 'tags',)
    list_filter = ('author', 'name', )
    empty_value_display = '-пусто-'

    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'indigrient')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(Rurchases)
class RurchasesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author')
    search_fields = ('author',)
    list_filter = ('author',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author',)
    list_filter = ('author',)
