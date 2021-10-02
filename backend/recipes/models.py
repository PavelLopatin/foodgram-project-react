from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False,
                            blank=False, verbose_name='Название тега')
    color = models.CharField(max_length=7, unique=True, null=False,
                             blank=False, verbose_name='Цвет')
    slug = models.CharField(max_length=200, unique=True, null=False,
                            help_text='Введите уникальный слаг',
                            blank=False, verbose_name='Уникальный слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False,
                            help_text='Введите название ингредиента',
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=200, null=False,
                                        help_text='Выберите меру измерения',
                                        blank=False, verbose_name='Мера измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False,
                            verbose_name='Название рецепта',
                            help_text='Введите название рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор',
                               help_text='Выберите автора')
    text = models.TextField(blank=False, null=False,
                            verbose_name='Описание',
                            help_text='Введите название ингредиента')
    tags = models.ManyToManyField(Tag, through='RecipeTags')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredients')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время готовки')
    image = models.ImageField(upload_to='recipes/images', blank=False, null=False,
                              verbose_name='Фото рецепта')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                   verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                         verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return 'Ингредиент в рецепте'


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            verbose_name='Тег')

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return 'Тег рецепта'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_favorite',
                               verbose_name='Рецепт')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_recipe_in_user_favorite')]


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_list',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_recipe_in_user_shopping_list')]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
