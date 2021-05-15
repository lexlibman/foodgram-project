from django import forms
from decimal import Decimal

from .models import Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    _objs = []

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

    def clean(self):
        ingredients = {}
        for key, name in self.data.items():
            if key.startswith('nameIngredient'):
                num = key.split('_')[1]
                ingredients[name] = self.data[
                    f'valueIngredient_{num}'
                ]
        for name, quantity in ingredients.items():
            try:
                ingredient = Ingredient.objects.get(title=name)
            except Ingredient.DoesNotExist:
                raise forms.ValidationError(
                    'Ингредиента нет в базе данных'
                )
            self._objs.append([ingredient, quantity])

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        objs = []
        for ingredient in self._objs:
            objs.append(
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient[0],
                    quantity=Decimal(ingredient[1].replace(',', '.'))
                )
            )
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.save_m2m()
        return instance
