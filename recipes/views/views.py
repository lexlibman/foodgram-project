from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, RecipeIngredient

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


def index(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    recipes = Recipe.objects.filter(
        tags__title__in=tags
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
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
        recipe = form.save_m2m()

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
        RecipeIngredient.objects.filter(recipe).delete()
        form.instance.author = request.user
        recipe = form.save_m2m()
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
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    author_recipes = author.recipes.filter(
        tags__title__in=tags
    ).prefetch_related('tags').distinct()

    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/authorRecipe.html',
        {
            'author': author,
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


@login_required
def subscriptions(request):
    authors = User.objects.filter(
        following__user=request.user
    ).prefetch_related(
        'recipes'
    ).annotate(recipe_count=Count('recipes')).order_by('username')

    paginator = Paginator(authors, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/myFollow.html',
        {
            'page': page,
            'paginator': paginator,
        }
    )


@login_required
def favorites(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    recipes = Recipe.objects.filter(
        favored_by__user=request.user,
        tags__title__in=tags
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/favorite.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
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
        file_text += line + '\n'

    response = HttpResponse(
        file_text, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
