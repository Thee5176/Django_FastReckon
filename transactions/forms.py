from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from datetime import datetime
from .models import Transaction, Entry

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date","book","description","shop","has_receipt"]
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type':'date',
                    'autocomplete':'off',
                },
            )
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['date'].initial = datetime.now().date() 
    
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["account","entry_type", "amount"]
        
EntryInlineFormSet = inlineformset_factory(Transaction, Entry, form=EntryForm, extra=0, min_num=2)