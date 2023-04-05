import io
from http import HTTPStatus

from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientAmount,
                            ListShopping, Recipe, Subscribe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.response import Response
from user.models import User

from api.filters import RecipeFilters

from .pagination import ProductsPagination
from .serializers import (FavoriteSerializer, IngredientAmountSerializer,
                          IngredientSerializer, ListShoppingSerializer,
                          RecipeCreateSerializer, RecipeInfodSerializer,
                          RecipeSerializer, SubscriptionSerializer,
                          TagSerializer, UserSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работе с моделью Tag"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работе с моделью Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для работе с моделью Favorite."""
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite
    permission_classes = (permissions.AllowAny,)


class DownloadCartViewSet(viewsets.ModelViewSet):
    queryset = ListShopping.objects.all()
    serializer_class = ListShoppingSerializer
    model = ListShopping

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            author=request.user, recipe=recipe)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, author__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class Cart(generics.ListAPIView):
    """Вьюсет для работе с моделью Cart."""
    def get(self, request):
        user = request.user
        list_filter = (ListShopping.objects.filter(author_id=user.id).
                       values_list("recipe", flat=True))
        recipe_filter = IngredientAmount.objects.filter(
            recipe_id__in=list_filter)
        recipes = {}
        for ingredient_mount in recipe_filter:
            z = ingredient_mount.amount
            if ingredient_mount.ingredients in recipes:
                recipes[ingredient_mount.ingredients] += z
            else:
                recipes[ingredient_mount.ingredients] = z
        wishlist = []
        wishlist.append('Список покупок:')
        for k, v in recipes.items():
            wishlist.append(f'{k.name} - {v}, {k.measurement_unit}\n')
        pdfmetrics.registerFont(TTFont('DejaVuSerif',
                                       './api/ttf/DejaVuSerif.ttf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("DejaVuSerif", 15)
        start = 800
        for line in wishlist:
            p.drawString(50, start, line)
            start -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='cart_list.pdf')


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работе с моделью Recipe."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilters
    pagination_class = ProductsPagination

    def get_serializer_class(self):
        """Функция выбора класса - сериализатора в зависимости от метода"""
        if self.request.method == "GET":
            return RecipeSerializer
        return RecipeCreateSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = ProductsPagination

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):

        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class CreateUserViewSet(UserViewSet):
    """Вьюсет для работе с моделью User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProductsPagination
    permission_classes = (permissions.AllowAny,)
