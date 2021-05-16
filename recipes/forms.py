from decimal import Decimal

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from recipes.models import Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'cooking_time',
            'text',
            'image',
        )
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, data=None, *args, **kwargs):
        self.ingredients = {}
        if data is not None:
            data = data.copy()
            self.get_ingredients(data)

        super().__init__(data=data, *args, **kwargs)

    def get_ingredients(self, data):
        for key, name in data.items():
            if key.startswith('nameIngredient'):
                _, _, number = key.partition('_')
                value = f'valueIngredient_{number}'
                self.ingredients[name] = {
                    'quantity': int(Decimal(data.get(value)).replace(',', '.'))
                }

    def clean(self):
        if not self.ingredients:
            raise forms.ValidationError(
                'Необходимо добавить хотя бы один ингредиент'
            )
        for title, quantity in self.ingredients.items():
            if quantity.get('quantity') < 0:
                raise forms.ValidationError(
                    f"Неверное количество для '{title}'"
                )
            try:
                ingredient = Ingredient.objects.filter(title=title).get()
                self.ingredients[title].update({'object': ingredient})
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    f"Ингредиента '{title}' нет в базе данных"
                )
        return super().clean()

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()
        objects = []
        for data in self.ingredients.values():
            objects.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=data.get('object'),
                    quantity=data.get('quantity'),
                )
            )
        if objects:
            recipe.ingredients_amounts.all().delete()
            RecipeIngredient.objects.bulk_create(objects)
        self.save_m2m()
        return recipe
