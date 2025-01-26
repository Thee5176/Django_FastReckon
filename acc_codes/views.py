
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from .models import Account, AccountLevel1, AccountLevel2, AccountLevel3
from .mixins import AccountColorCodeMixin
from accounts.mixins import UserOwnedQuerysetMixin
from acc_books.models import Book
from transactions.models import Transaction, Entry

class AccountListView(AccountColorCodeMixin, UserOwnedQuerysetMixin, ListView):
    model = Account
    template_name = "acc_codes/account_list.html"      

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        code = self.request.GET.get("code")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__startswith=code) 
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AccountDetailView(LoginRequiredMixin, AccountColorCodeMixin, UserOwnedQuerysetMixin, DetailView):
    model = Account
    template_name = "acc_codes/account_detail.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("level3__level2__level1")
        return queryset    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()
        if obj:
            context["entry_list"] = Entry.objects.select_related('transaction__book').filter(code=obj.id)
            book = Book.objects.get(transactions=context['entry_list'].first().transaction)
            context["currency_sign"] = book.currency_sign
        return context

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","level3","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","level3","sub_account","detailed_account","guideline"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    template_name = "journals/account_delete.html"
    success_url = reverse_lazy("account_list")

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user