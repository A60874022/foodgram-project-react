from rest_framework import viewsets 

from rest_framework import serializers
from recipes.models import (Indigrient, Recipe, IngredientAmount,
                            Tags, Favourites, Rurchases, Follow)
from rest_framework import generics, filters, mixins, permissions, status, viewsets
from user.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from django import HttpResponse

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

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