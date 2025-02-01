
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView

from .models import Account
from accounts.mixins import UserOwnedQuerysetMixin
from acc_books.models import Book
from transactions.models import Entry

class AccountListView(LoginRequiredMixin, UserOwnedQuerysetMixin, ListView):
    model = Book
    template_name = "acc_codes/account_list.html"      

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        code = self.request.GET.get("code")
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if code:
            queryset = queryset.filter(account__startswith=code) 
        
        return queryset

class AccountDetailView(LoginRequiredMixin, UserOwnedQuerysetMixin, DetailView):
    model = Account
    template_name = "acc_codes/account_detail.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.get_object()
        if obj:
            context["entry_list"] = Entry.objects.filter(account=obj.id).order_by("transaction__date")

        return context

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "acc_codes/account_alter_form.html"
    fields = ["name","root","sub_account","detailed_account","guideline","book"]
    
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
    fields = ["name","root","sub_account","detailed_account","guideline"]
    
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
    
from django.shortcuts import render,get_object_or_404

def filter_account_by_book(request):
    if request.method == "POST":
        query = request.POST.get("book-filter")
        
        if query and query != "all":
            book_filter = get_object_or_404(Book, pk=query)
            print(f"{book_filter.abbr} Book is selected.")
            book_instance = [book_filter]
        else:
            book_instance = Book.objects.all()
            print(f"{len(book_instance)} Books are selected.")
        
        return render(request, "acc_codes/partials/base_acc_table.html", {'book_list':book_instance})