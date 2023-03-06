from rest_framework import viewsets 

from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from rest_framework import generics, filters, mixins, permissions, viewsets
from user.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from django import HttpResponse

from .permissions import IsAuthorOnly

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

class IndigrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Indigrient.objects.all()
    serializer_class = IndigrientSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name')
    permission_classes = (IsAuthorOnly,) 

class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Favourites.objects.all()
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('favorites__user', 'author', 'tags', 'rurchases_user')
    serializer_class = RecipeSerializer
    pagination_class = ProductsPagination

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return RecipeCreateSerializer
        elif self.request.method == "GET":
            return RecipeSerializer

class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = ProductsPagination
    permission_classes = (permissions.AllowAny,)

class FollowCreateViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin ,
                            viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
   
    
 