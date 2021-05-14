from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest

from .models import RecipeIngredient, Tag


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def edit_recipe(form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return form.save()
    except IntegrityError:
        raise HttpResponseBadRequest


def create_paginator(items_list, number_of_items, request):
    paginator = Paginator(items_list, number_of_items)
    page_number = request.GET.get('page')
    return paginator, page_number


def turn_on_tags():
    return (
        '?filter='
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
