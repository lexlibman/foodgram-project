from django.contrib import admin
from django.db.models import Count

from . import models


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    min_num = 1
    extra = 0
    verbose_name = 'ингредиент'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = (
        'id', 'title', 'author', 'slug',
        'cooking_time', 'get_favorite_count', 'pub_date'
    )
    list_filter = ('author', 'tags__title')
    search_fields = ('title', 'author__username')
    autocomplete_fields = ('author', )
    ordering = ('-pub_date', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('favored_by'))

    def get_favorite_count(self, obj):
        return obj.favorite_count


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('^title', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'display_name')
    list_filter = ('title', )


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    autocomplete_fields = ('user', 'author')


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
