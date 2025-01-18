from django import forms
from django.forms import modelformset_factory

from prepcards.models import PrepCard, IngredientUsed


class PrepCardForm(forms.ModelForm):
    
    class Meta:
        model = PrepCard
        fields = (
        "date",
        "duration"
        )

class IngredientForm(forms.ModelForm):
    
    class Meta:
        model = IngredientUsed
        fields = (
        "name",
        "amount_of_unit"
        )
        
IngredientFormSet = modelformset_factory(
    IngredientUsed, 
    form=IngredientForm,
    min_num=1,
    extra=0,
    can_delete=True
)