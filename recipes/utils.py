from django.core.paginator import Paginator
from rest_framework.generics import get_object_or_404

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


def save_recipe(ingredients, recipe):
    recipe_ingredients = []

    for title, value in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        rec_ingredient = RecipeIngredient(
            value=value, ingredient=ingredient, recipe=recipe
        )
        recipe_ingredients.append(rec_ingredient)

    RecipeIngredient.objects.bulk_create(recipe_ingredients)


def create_paginator(items_list, number_of_items, request):
    paginator = Paginator(items_list, number_of_items)
    page_number = request.GET.get('page')
    return paginator, page_number


def turn_on_tags():
    return (
        '?filter='
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
