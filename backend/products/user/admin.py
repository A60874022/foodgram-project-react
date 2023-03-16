from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Класс для работы таблицы пользователь.
    """
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
