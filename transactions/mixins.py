from django.shortcuts import redirect

from .forms import TransactionForm, EntryInlineFormSet
from .models import Transaction

class TransactionFormValidator:
    """
    Form Checklist:
    - Dr/Cr Balance
    - Assign intra-month-ref
    Form Auto-filled:
    - Transaction.created_by = self.get_object().user
    - Entry.transaction = self.get_object()
    """
    
    def form_valid(self, form):
        """
        Add validation for additional form context: EntryFormSet
        """
        transaction = form.save(commit=False)       #this is the model's object itself
        formset = EntryInlineFormSet(self.request.POST, instance=transaction)
        
        if formset.is_valid():
            new_entries = formset.save(commit=False)
            print(new_entries)
            for entry in formset.deleted_objects:
                entry.delete()
            
            #if new record (yet to assign pk) will return empty list()
            if formset.instance.pk:
                new_entries_pk = [entry.pk for entry in new_entries]
                old_entries = list(formset.instance.entries.exclude(pk__in=new_entries_pk))
            else:
                old_entries = list()
                
            all_entries = new_entries + old_entries
            
            if not transaction.is_balance(all_entries):
                formset.non_form_errors().append(
                    f"Amount is invalid. - Dr/Cr Amount :"
                    f"{transaction.total_debits(all_entries)}/{transaction.total_credits(all_entries)}"
                )
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset)
                )
                
            #Assign User before save transaction
            transaction.created_by = self.request.user
            transaction.save()
            
            #Assign transaction before save to entries
            try:
                for entry in all_entries:
                    entry.transaction = transaction
                    entry.save()   
            except Exception as e:
                print("Error saving entry:", e)

            #Send list of account instance via session
            self.request.session['account_pk_list'] = [entry.account.pk for entry in all_entries]
            print(f"Save session: {all_entries}")
        else:
            print("formset value not valid")
            
        return redirect('transaction_confirm', slug=transaction.slug)
        
    def form_invalid(self, form):
        """
        Add validation for additional form context: EntryFormSet
        """
        formset = EntryFormset(self.request.POST)
        print("Transaction Form is invalid")
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
