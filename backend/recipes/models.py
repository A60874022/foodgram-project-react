from django.core.validators import MinValueValidator
from django.db import models

from user.models import User


class Indigrient(models.Model):
    """Класс для работы таблицы Ингредиент."""
    name = models.CharField(max_length=200, verbose_name='Название',)
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Еденица измерения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        models.UniqueConstraint(fields=['name', 'following'],
                                name='measurement_unit')

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
    indigrients = models.ManyToManyField(
        Indigrient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        'Tag',
        through='TagRecipe',
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
    quantity = models.FloatField(verbose_name='количество', blank=True,
                                 validators=(MinValueValidator(1,
                                                               'Минимальное'
                                                               'количество'
                                                               'ингредиентов'
                                                               '1'),),)

    class Meta:
        verbose_name = 'Рецепт -интигриенты'
        verbose_name_plural = 'Рецепт -интигриенты'

    def __str__(self):
        return f'{self.recipe}{self.indigrient}'


class Tag(models.Model):
    """Класс для работы таблицы тэг."""
    name = models.CharField(max_length=200,
                            verbose_name='Название',)
    color = models.CharField(max_length=7, default="#ffffff",
                             verbose_name='цвет')
    slug = models.SlugField(unique=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Выберите теги рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(fields=['tag', 'recipe'],
                                    name='unique_tagrecipe')
        ]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    """Класс для работы таблицы Избранное."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='Favorite',
                               verbose_name='рецепты')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='Favorite',
                             verbose_name='пользователи')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return f'{self.recipe} {self.user}'


class ListShopping(models.Model):
    """Класс для работы таблицы списка покупок."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ListShopping',
                               verbose_name='рецепты')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='ListShopping',
                               verbose_name='автор')

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'

    def __str__(self):
        return f'{self.author} {self.recipe}'


class Follow(models.Model):
    """Класс для работы таблицы подписки на авторов."""
    user = models.ForeignKey(User, blank=True,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='подписчики')
    author = models.ForeignKey(User, blank=True,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='автор')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'подписчики'
        models.UniqueConstraint(fields=['user', ' author'],
                                name='unique_subscribe')

    def __str__(self):
        return f'{self.user} {self.author}'