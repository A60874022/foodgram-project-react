from api.views import (Cart, CreateUserViewSet, DownloadCartViewSet,
                       FavoriteViewSet, FollowCreateViewSet, FollowViewSet,
                       IndigrientViewSet, RecipeViewSet, TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', CreateUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredient', IndigrientViewSet, basename='ingredient')

urlpatterns = [
    path('recipes/download_shopping_cart/',
         DownloadCartViewSet.as_view(({'get': 'list'})), name='ListShopping'),
    path('recipes/<int:id>/shopping_cart/', Cart.as_view(),
         name='dowload_shopping_cart'),
    path('recipes/<int:id>/favorite/', FavoriteViewSet.as_view,
         name="favorite"),
    path('users/subscriptions/', FollowViewSet.as_view(({'get': 'list'}))),
    path('users/<int:id>/subscribe/',
         FollowCreateViewSet.as_view({'post': 'create',
                                      'delete': 'delete'}),
         name='subscribe'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls))
]
