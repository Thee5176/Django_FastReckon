from django import forms
from django.forms import modelformset_factory
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
                    'class':'datepicker',
                    'autocomplete':'off',
                    'value':datetime.today().strftime('%Y-%m-%d')
                },
            )
        }
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["code","entry_type", "amount"]
        
EntryFormSet = modelformset_factory(Entry, form=EntryForm, extra=2)
EntryFormSet_update = modelformset_factory(Entry, form=EntryForm, extra=0)
