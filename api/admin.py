from django.contrib import admin

from .models import Favorite, Purchase, Subscription


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('ID', 'пользователь', 'рецепт')
    autocomplete_fields = ('user', 'recipe')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('ID', 'пользователь', 'автор')
    autocomplete_fields = ('user', 'author')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('ID', 'пользователь', 'рецепт')
    autocomplete_fields = ('user', 'recipe')
