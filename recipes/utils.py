from decimal import Decimal

from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient, Recipe


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
    except IntegrityError:
        raise HttpResponseBadRequest


def edit_recipe(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


def get_purchase_recipes_from_session(session):
    recipes_ids = session.get('recipe_ids')
    if recipes_ids is not None:
        recipes = Recipe.objects.filter(pk__in=recipes_ids)
        return recipes


def create_shop_list(session):
    recipes = get_purchase_recipes_from_session(session)
    ingredients = recipes.order_by('ingredients__title').values(
        'ingredients__title',
        'ingredients__dimension').annotate(
        total_amount=Sum('ingredient_amounts__amount'))
    filename = 'shopping_list.txt'
    content = ''
    for ingredient in ingredients:
        string = (f'{ingredient["ingredients__title"]} '
                  f'({ingredient["ingredients__dimension"]}) — '
                  f'{ingredient["total_amount"]}')
        content += string + '\n'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
