from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import 

app_name = 'api'

router = DefaultRouter()
# Вызываем метод .register с нужными параметрами
router.register('users', UserViewSet, name = 'users')
router.register('tags', TagsViewSet, name = 'tags')
router.register('recipes', RecipeViewSet, name = 'recipes')
router.register('ingredients',IndigrientViewSet, name = 'ingredients')

urlpatterns = [
 
    path('recipes/download_shopping_cart/',  DownloadCartViewSet, name = 'rurchases'),
    path('recipes/<int:id>/download_shopping_cart/', Cart.as_view(), name = 'rurchases'),
    path('recipes/<int:id>/favorites/', FavoriteViewSet),
    path('users/subscriptions/', FollowViewSet),
    path('/users/<int:id>/subscriptions/', FollowCreateViewSet),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]