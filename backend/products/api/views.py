from http import HTTPStatus

from api.filters import RecipeFilters
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, Indigrient, ListShopping, Recipe,
                            Tag)
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.response import Response
from user.models import User

from .pagination import ProductsPagination
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IndigrientSerializer, ListShoppingSerializer,
                          RecipeCreateSerializer, RecipeInfodSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работе с моделью Tag"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IndigrientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работе с моделью Indigrient."""
    queryset = Indigrient.objects.all()
    serializer_class = IndigrientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для работе с моделью Favorite."""
    queryset = Recipe.objects.all()
    serializer_class = FavoriteSerializer


class DownloadCartViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = ListShopping.objects.all()
    serializer_class = ListShoppingSerializer


class Cart(generics.ListAPIView):
    """Вьюсет для работе с моделью Favorite."""
    def get(self, request):
        filename = 'test.txt'
        queryset = Favorite.objects.all()
        serializer = FavoriteSerializer(queryset)
        response = HttpResponse(serializer.data,
                                content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = ('attachment;'
                                           'filename={0}'.format(filename))
        return response


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работе с моделью Recipe."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilters
    serializer_class = RecipeSerializer
    pagination_class = ProductsPagination

    def get_serializer_class(self):
        """Функция выбора класса - сериализатора в зависимости от метода"""
        if self.request.method in ["POST", "PATCH"]:
            return RecipeCreateSerializer
        elif self.request.method == "GET":
            return RecipeSerializer


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работе с моделью Follow."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeInfodSerializer
    permission_classes = (permissions.AllowAny,)


class FollowCreateViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """Вьюсет для работе с моделью Follow."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def delete(self, request, *args, **kwargs):
        """Переопределение метода delete."""
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class CreateUserViewSet(UserViewSet):
    """Вьюсет для работе с моделью User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProductsPagination
