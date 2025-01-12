# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from .forms import MyIngredientForm
from .models import Ingredient

class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "ingredients/ingredient_list.html"
    
class IngredientCreateView(LoginRequiredMixin, FormView):
    form_class = MyIngredientForm
    template_name = "ingredients/ingredient_alter_form.html"
    success_url = reverse_lazy("ingredient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        return context
    
    
class IngredientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = MyIngredientForm
    template_name = "ingredients/ingredient_alter_form.html"
    success_url = reverse_lazy("ingredient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

class IngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingredient
    template_name = "ingredients/ingredient_delete.html"
    success_url = reverse_lazy("ingredient_list")

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
