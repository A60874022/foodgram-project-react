from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class Indigrient(models.Model):
    """Класс для работы таблицы Ингредиент."""
    name = models.CharField(max_length=200, verbose_name='Название',)
    unit_of_measurement = models.CharField(max_length=200,
                                           verbose_name='Еденица измерения')
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс для работы таблицы Рецепты."""
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=200, verbose_name='Название',)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(verbose_name='Текст рецепта')
    indigrient = models.ManyToManyField(
        Indigrient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        'Tags',
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время должно быть больше 1 минуты'),),
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """
    Класс для работы таблицы ингредиенты и рецепты.
    Таблица для связи - многие к многим.
    """
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='IngredientAmount',
                               verbose_name='Рецепт')
    indigrient = models.ForeignKey(Indigrient,
                                   on_delete=models.CASCADE,
                                   related_name='IngredientAmount',
                                   verbose_name='Ингредиент')
    quantity = models.FloatField(verbose_name='количество',
                                 validators=(MinValueValidator(1,
                                                               'Минимальное'
                                                               'количество'
                                                               'ингредиентов'
                                                               '1'),),)
    
    class Meta:
        verbose_name = 'Рецепт -интигриенты'
        verbose_name_plural = 'Рецепт -интигриенты'


    def __str__(self):
         return f' {self.recipe}{self.indigrient}'



class Tags(models.Model):
    """Класс для работы таблицы тэг."""
    name = models.CharField(max_length=200,
                            verbose_name='Название',)
    hexcolor = models.CharField(max_length=7, default="#ffffff", 
                                verbose_name = 'цвет')
    slug = models.SlugField(unique=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Favourites(models.Model):
    """Класс для работы таблицы Избранное."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favourites',
                               verbose_name='рецепты')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites',
                             verbose_name='пользователи')
    
    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
    
    def __str__(self):
        return self.recipe

      
class Rurchases(models.Model):
    """Класс для работы таблицы списка покупок."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='rurchases',
                               verbose_name='рецепты')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rurchases',
                               verbose_name='автор')
    
    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural= 'список покупок'
    
    def __str__(self):
        return f'{self.user} {self.recipe}'


class Follow(models.Model):
    """Класс для работы таблицы подписки на авторов."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='подписчики')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='автор')
    
    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'подписчики'

    def __str__(self):
        return f'{self.user} {self.following}'
