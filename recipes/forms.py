from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, Recipe


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

    def clean(self):
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        for id in known_ids:
            title = self.data.get(f'nameIngredient_{id}')
            value = self.data.get(f'valueIngredient_{id}')

            if int(value) <= 0:
                raise ValidationError('Ингредиентов должно быть больше 0')

            is_exists = Ingredient.objects.filter(
                title=title).exists()

            if not is_exists:
                raise ValidationError('Выберите ингредиент из списка')
