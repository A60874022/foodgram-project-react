from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import CatViewSet

app_name = 'api'

router = DefaultRouter()
# Вызываем метод .register с нужными параметрами
router.register('users', AdminUser, name = 'users')
router.register('tags', AdminUser, name = 'tags')
router.register('recipes', AdminUser, name = 'recipes')
router.register('ingredients', AdminUser, name = 'ingredients')

urlpatterns = [
    path('user/me', ),
    path('recipes/download_shopping_cart/', ),
    path('recipes/<int:id>/download_shopping_cart/', ),
    path('recipes/<int:id>/favorites/', ),
    path('recipes/users/subscriptions/', ),
    path('recipes/users/<int:id>/subscriptions/', ),
]