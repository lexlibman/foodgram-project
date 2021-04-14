from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


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
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        objs = []
        ingredients = get_ingredients(request)
        for name, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=name)
            objs.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=Decimal(quantity.replace(',', '.'))
                )
            )
        RecipeIngredient.objects.bulk_create(objs)
        form.save_m2m()
        return recipe


def edit_recipe(request, form, instance):
    with transaction.atomic():
        RecipeIngredient.objects.filter(recipe=instance).delete()
        return save_recipe(request, form)
