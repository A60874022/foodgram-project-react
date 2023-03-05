from rest_framework import viewsets 

from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from user.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class IndigrientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Indigrient.objects.all()
    serializer_class = IndigrientSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name')

class  DownloadCartViewSet(ListModelMixin, CreateModelMixin, 
                            DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Rurchases.objects.all()
    serializer_class = RurchasesSerializer

class FavoriteViewSet(CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Favourites.objects.all()
    serializer_class =FavouritesSerializer
