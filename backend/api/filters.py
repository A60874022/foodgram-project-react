from django_filters import rest_framework as django_filter
from rest_framework import filters
from recipes.models import Recipe
from user.models import User


class RecipeFilters(django_filter.FilterSet):
    author = django_filter.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filter.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filter.BooleanFilter(method='get_is_favorited',
                                               label='is_favorited')
    is_in_shopping_cart = django_filter.BooleanFilter(
        method='get_is_in_shopping_cart', label='is_in_shopping_cart')

    class Meta:

        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(carts__user=self.request.user)
        return queryset


class IngredientSearchFilter(filters.SearchFilter):

    search_param = 'name'
