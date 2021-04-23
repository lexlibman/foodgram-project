from django import template
from django.contrib.auth import get_user_model

from recipes.models import Favorite, Purchase, Subscription

register = template.Library()
User = get_user_model()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def is_subscribed_to(user, author):
    return Subscription.objects.filter(user=user, author=author)


@register.filter
def is_favored_by(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user)


@register.filter
def is_in_shop_list_of(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user)


@register.filter
def get_full_name_or_username(user):
    return user.get_full_name() or user.username
