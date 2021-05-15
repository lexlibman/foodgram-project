from django import forms

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
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, num = items.split('_')
                known_ids.append(num)
        for num in known_ids:
            title = self.data.get(f'nameIngredient_{num}'),
            dimension = self.data.get(f'unitsIngredient_{num}')
            try:
                self._objs.append(
                    Ingredient.objects.filter(
                        title=title[0],
                        dimension=dimension,
                    )
                )
            except Ingredient.DoesNotExist:
                raise forms.ValidationError(
                    'Ингредиента нет в базе данных'
                )

    def save(self, commit=True):
        return RecipeIngredient.objects.bulk_create(self._objs)
