from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.shortcuts import get_object_or_404
from datetime import datetime

from .forms import TransactionForm, EntryInlineFormSet
from .models import Transaction, Entry
from .mixins import TransactionFormValidator
from acc_codes.models import Account
from acc_books.models import Book
from accounts.mixins import UserOwnedQuerysetMixin

class TransactionListView(LoginRequiredMixin, UserOwnedQuerysetMixin, ListView):
    model = Book
    template_name = "transactions/transaction_list.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        kw = self.request.GET.get("keyword")
        date = self.request.GET.get("created")
        
        if kw:
            queryset = queryset.filter(
                Q(description__icontains=kw)| Q(slug__icontains=kw) | Q(shop__icontains=kw)
            )
            
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(created__date=date_obj)
                print(f"Filtering by date: {date_obj}")
            except ValueError:
                print(f"Invalid date format: {date}")
                
        return queryset    

class TransactionDetailView(LoginRequiredMixin, UserOwnedQuerysetMixin, DetailView):
    model = Transaction
    template_name = "transactions/transaction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entries"] = Entry.objects.select_related('transaction','code__root').filter(transaction_id=transaction.id)
        return context

class TransactionCreateView(LoginRequiredMixin, TransactionFormValidator, FormView):
    form_class = TransactionForm        
    template_name = "transactions/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry_formset"] = EntryInlineFormSet(queryset=Entry.objects.none())
        context["view_name"] = "Create"
        return context
        
class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, TransactionFormValidator, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/transaction_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction = self.get_object()
        context["entry_formset"] = EntryInlineFormSet(instance=transaction)
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    
class TransactionConfirmView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Transaction
    template_name = "transactions/confirm_account_balance.html"

    def test_func(self):
        self.account_list = self.request.session.get("account_list")
        if self.account_list:
            obj = self.get_object()
        return obj.created_by == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.account_list:        # Session data loaded in test_func
            context["account_list"] = Account.objects.filter(code__in=self.account_list)
        transaction = self.get_object()
        context["entries"] = transaction.entries.all()
        return context
    
class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = "transactions/transaction_delete.html"
    success_url = reverse_lazy("transaction_list")
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

from django.shortcuts import render
from django.forms import inlineformset_factory
from .forms import EntryForm

def add_entry_form(request):
    if request.method == "POST":
        # get current form count
        total_forms = int(request.POST.get("entries-TOTAL_FORMS",0)) + 1
        print("Total forms: ",total_forms)
        EntryForm_extra = inlineformset_factory(Transaction, Entry, form=EntryForm, max_num=total_forms)
        new_forms = EntryForm_extra(queryset=Entry.objects.none())[-1]
        
        return render(request, "transactions/partials/entry_form.html", {"form" : new_forms})
    
def filter_transaction_by_book(request):
    if request.method == "POST":
        query = request.POST.get("book-filter")
        
        if query and query != "all":
            book_filter = get_object_or_404(Book, pk=query)
            print(f"{book_filter.abbr} Book is selected.")
            book_instance = [book_filter]
        else:
            book_instance = Book.objects.all()
            print(f"{len(book_instance)} Books are selected.")
        
        return render(request, "transactions/partials/base_tran_table.html", {'book_list':book_instance})