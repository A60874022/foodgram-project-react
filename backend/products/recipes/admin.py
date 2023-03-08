from django.contrib import admin

from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)


class IndigrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_of_measurement')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',
                    'amount_tags', 'amount_ingredients')
    search_fields = ('author','name', 'tags',)
    list_filter = ('author', 'name', )
    empty_value_display = '-пусто-'

    
    @staticmethod
    def amount_tags(obj):
        return "\n".join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    def amount_ingredients(obj):
        return "\n".join([i[0] for i in obj.ingredients.values_list('name')])

class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'indigrient')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

    
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('user',)
    list_filter = ('user',)


class RurchasesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author')
    search_fields = ('author',)
    list_filter = ('author',)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author',)
    list_filter = ('author',)

admin.site.register(Indigrient, IndigrientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(Rurchases, RurchasesAdmin)
admin.site.register(Follow, FollowAdmin)