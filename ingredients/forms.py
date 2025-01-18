from django import forms

from .models import Ingredient

class MyIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            "name",
            "category",
            "unit",
            "cost_per_unit",
        )