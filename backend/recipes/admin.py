from django.contrib import admin

from recipes.models import (Favorite, Follow, Indigrient, IngredientAmount,
                            ListShopping, Recipe, Tag)


class IndigrientInline(admin.StackedInline):
    model = Recipe.indigrients.through


class TagtInline(admin.StackedInline):
    model = Recipe.tags.through


@admin.register(Indigrient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'indigrient')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',
                    'amount_tag', 'amount_ingredient')
    search_fields = ('author', 'name', 'tags',)
    list_filter = ('author', 'name', )
    empty_value_display = '-пусто-'
    inlines = [IndigrientInline, TagtInline, ]

    @staticmethod
    def amount_tag(obj):
        return "\n".join([i[0] for i in obj.Tag.values_list('name')])

    @staticmethod
    def amount_ingredient(obj):
        return "\n".join([i[0] for i in obj.ingredient.values_list('name')])


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


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author',)
    list_filter = ('author',)
