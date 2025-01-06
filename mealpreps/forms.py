from django import form
from django.form import 
from mealpreps.models import PrepCard, IngredientUsed

class PrepCardForm(forms.ModelForm):
    
    class Meta:
        model = PrepCard
        fields = ("owner","date","duration")

class IngredientForm(forms.ModelForm):
    
    class Meta:
        model = IngredientUsed
        fields = ("name","amount","catagory")

IngredientFormSet = modelformset_factory(IngredientUsed, form=IngredientForm, extra=10)