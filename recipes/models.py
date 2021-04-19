from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class RecipeQuerySet(models.QuerySet):

    def get_additional_attributes(self, user, tags=None):
        if user.is_authenticated:
            favorite = Favorite.objects.filter(
                recipe=models.OuterRef('pk'),
                user=user
            )
            purchase = Purchase.objects.filter(
                recipe=models.OuterRef('pk'),
                user=user
            )
            subscription = Subscription.objects.filter(
                author=models.OuterRef('author'),
                user=user
            )
            if tags:
                return self.filter(
                    tags__in=tags
                ).annotate(
                    favorite_flag=models.Exists(favorite),
                    shoplist_flag=models.Exists(purchase),
                    follow_flag=models.Exists(subscription)
                )
            return self.annotate(
                favorite_flag=models.Exists(favorite),
                shoplist_flag=models.Exists(purchase),
                follow_flag=models.Exists(subscription)
            )
        return self


class Ingredient(models.Model):
    title = models.CharField(
        'Название ингредиента',
        max_length=150,
        db_index=True
    )
    dimension = models.CharField('Единица измерения', max_length=10)

    class Meta:
        ordering = ('title', )
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    title = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Изображение', upload_to='recipes/')
    text = models.TextField('Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент'
    )
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    slug = AutoSlugField(populate_from='title', allow_unicode=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts'
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ('ingredient', 'recipe')


class Tag(models.Model):
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favored_by',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписался на',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в покупках',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
