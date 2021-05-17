from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.utils import create_paginator, turn_on_tags

User = get_user_model()


def index(request):
    tags = request.existing_tags
    if not tags:
        return redirect(f"{reverse('index')}{turn_on_tags()}")

    recipes = Recipe.objects.get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    context = {}

    return create_paginator(
        request,
        'recipes/index.html',
        context,
        recipes,
    )


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)

    return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug
    )

    return render(request, 'recipes/singlePage.html', {'recipe': recipe})


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save()

        return redirect(
            'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
        )

    return render(request, 'recipes/formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect(
                'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
            )

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save()
        return redirect(
            'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
        )

    return render(
        request,
        'recipes/formRecipe.html',
        {'form': form, 'recipe': recipe}
    )


@login_required
def recipe_delete(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    tags = request.existing_tags
    if not tags:
        return redirect(f"{reverse('profile_view', args=[author.username])}"
                        f'{turn_on_tags()}')
    author_recipes = Recipe.objects.filter(
        author=author
    ).get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    context = {'author': author}

    return create_paginator(
        request,
        'recipes/authorRecipe.html',
        context,
        author_recipes,
    )


@login_required
def subscriptions(request):
    authors = User.objects.filter(
        following__user=request.user
    ).prefetch_related(
        'recipes'
    ).annotate(recipe_count=Count('recipes')).order_by('username')
    context = {}

    return create_paginator(
        request,
        'recipes/myFollow.html',
        context,
        authors,
    )


@login_required
def favorites(request):
    tags = request.existing_tags
    if not tags:
        return redirect(f"{reverse('favorites')}{turn_on_tags()}")
    recipes = Recipe.objects.filter(
        favored_by__user=request.user
    ).get_additional_attributes(
        request.user,
        tags
    ).distinct().select_related(
        'author'
    )
    context = {}

    return create_paginator(
        request,
        'recipes/favorite.html',
        context,
        recipes,
    )


@login_required
def purchases(request):
    recipes = request.user.purchases.all()
    return render(
        request,
        'recipes/shopList.html',
        {'recipes': recipes},
    )


@login_required
def purchases_download(request):
    ingredients = request.user.purchases.select_related(
        'recipe'
    ).order_by(
        'recipe__ingredients__title'
    ).values(
        'recipe__ingredients__title', 'recipe__ingredients__dimension'
    ).annotate(amount=Sum('recipe__ingredients_amounts__quantity')).all()

    file_text = ''

    for item in ingredients:
        title, dimension, quantity = item.values()
        line = f'{title.capitalize()} ({dimension}) - {quantity}'
        file_text += line + '\r\n'

    response = HttpResponse(
        file_text, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
