from django.db import models
from django.core.validators import MinValueValidator
from user.models import User

class Indigrient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название',)
    unit_of_measurement =  models.CharField(max_length=200, verbose_name='Еденица измерения')

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=200, verbose_name='Название',)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    text = models.TextField( verbose_name='Текст рецепта')
    indigrient =models.ManyToManyField(
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


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='IngredientAmount',
        verbose_name='Рецепт'
    )
    indigrient = models.ForeignKey(Indigrient,
        on_delete=models.CASCADE,
        related_name='IngredientAmount',
        verbose_name='Ингредиент'
    )
    quantity = models.FloatField(verbose_name='количество')
class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название',)
    hexcolor = models.CharField(max_length=7, default="#ffffff")
    slug = models.SlugField(unique=True)




class Favourites(models.Model):
    recipe = models.ForeignKey(Recipe,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    user = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='favourites')


class Rurchases(models.Model):
    recipe = models.ForeignKey(Recipe,
                             on_delete=models.CASCADE,
                             related_name='rurchases')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rurchases')
                               

class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')


