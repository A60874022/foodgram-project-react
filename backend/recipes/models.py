from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class Ingredient(models.Model):
    """Класс для работы таблицы Ингредиент."""
    name = models.CharField(max_length=200, verbose_name='Название',)
    measurement_unit = models.CharField(max_length=200,
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
    ingredients = models.ManyToManyField(
        Ingredient,
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
                               related_name='IngredientRecipe',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='IngredientAmount',
                                   verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0, "Количество не может быть отрицательным"),
        ],
        verbose_name="Количество")

    class Meta:
        verbose_name = 'Рецепт -интигриенты'
        verbose_name_plural = 'Рецепт -интигриенты'

    def __str__(self):
        return f'{self.recipe}{self.ingredient}'


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
                               related_name='purchases',
                               verbose_name='автор')

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'

    def __str__(self):
        return f'{self.author} {self.recipe}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_subscribe')
        ]

    def __str__(self):

        return f'{self.user} {self.following}'
