from api.views import (Cart, CreateUserViewSet, DownloadCartViewSet,
                       FavoriteViewSet, FollowCreateViewSet, FollowViewSet,
                       IngredientViewSet, RecipeViewSet, TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', CreateUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', Cart.as_view(),
         name='ListShopping'),
    path('recipes/<recipes_id>/shopping_cart/',
         DownloadCartViewSet.as_view({'post': 'create',
                                      'delete': 'delete'}), name='cart'),
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
