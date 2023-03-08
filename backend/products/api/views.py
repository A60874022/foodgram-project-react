from rest_framework import viewsets 
from rest_framework.response import Response
from http import HTTPStatus
from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from rest_framework import generics, filters, mixins, permissions, viewsets
from user.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_list_or_404,  get_object_or_404
from rest_framework import permissions
from django.http import HttpResponse

from .permissions import IsAuthorOnly
from .pagination import ProductsPagination
from .serializers import (TagsSerializer, RecipeSerializer, RecipeCreateSerializer,
IndigrientSerializer, FavouritesSerializer, RurchasesSerializer,
RecipeInfodSerializer, FollowSerializer, UserSerializer)
from api.filters import RecipeFilters

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
    pagination_class = None

class IndigrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Indigrient.objects.all()
    serializer_class = IndigrientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthorOnly,) 
    pagination_class = None

class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class =FavouritesSerializer

class  DownloadCartViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, 
                           viewsets.GenericViewSet):
    queryset = Rurchases.objects.all()
    serializer_class = RurchasesSerializer

class Cart(generics.ListAPIView):

    def get(self, request):
        filename = 'test.txt'
        queryset = Favourites.objects.all()
        serializer =FavouritesSerializer(queryset)
        response = HttpResponse(serializer.data, content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = ('attachment; filename={0}'.format(filename))
        return response

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilters
    serializer_class = RecipeSerializer
    pagination_class = ProductsPagination

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return RecipeCreateSerializer
        elif self.request.method == "GET":
            return RecipeSerializer

class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class =  RecipeInfodSerializer
   
    permission_classes = (permissions.AllowAny,)

class FollowCreateViewSet(mixins.DestroyModelMixin, mixins.CreateModelMixin, 
                            viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


    def delete(self, request, *args, **kwargs):

        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)
   

        
class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin,  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = ProductsPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
 