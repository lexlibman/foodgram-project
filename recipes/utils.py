from django.core.paginator import Paginator
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django import forms

from .models import Ingredient, RecipeIngredient, Tag


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            form.instance.author = request.user
            recipe = form.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, quantity in ingredients.items():
                try:
                    ingredient = Ingredient.objects.get(title=name)
                except Ingredient.DoesNotExist:
                    raise forms.ValidationError(
                        'Такого ингредиента нет в базе данных('
                    )
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def edit_recipe(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


def create_paginator(items_list, number_of_items, request):
    paginator = Paginator(items_list, number_of_items)
    page_number = request.GET.get('page')
    return paginator, page_number


def turn_on_tags():
    return (
        f"?filter="
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
