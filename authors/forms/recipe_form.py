from django import forms
from recipes.models import Recipe


class AuthorRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings', 'preparation_step', 'preparation_step_is_html', 'cover'
