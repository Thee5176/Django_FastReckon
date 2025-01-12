from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin, 
)
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, DeleteView

from .mixins import CustomFormValidator
from .models import PrepCard, IngredientUsed
from .forms import PrepCardForm, IngredientForm, IngredientFormSet
# TODO: turn template into calendar archive view

class PrepListView(LoginRequiredMixin, ListView):
    model = PrepCard
    template_name = "prepcards/prepcard_list.html"
    
class PrepCreateView(LoginRequiredMixin, CustomFormValidator, FormView):
    form_class = PrepCardForm
    template_name = "prepcards/prepcard_alter_form.html"
    success_url = reverse_lazy("prepcard_list")    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        context["formset"] = IngredientFormSet(None)
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            mycard = form.save(commit=False)
            formset = IngredientFormSet(self.request.POST)
            if formset.is_valid():
                myingredient = formset.save(commit=False)
                for item in myingredient:
                    item.card = mycard
                
            mycard.created_by = self.request.user
            mycard.save()
            
            for item in myingredient:
                item.save()

        return super().form_valid(form)
    
    
class PrepUpdateView(LoginRequiredMixin, UserPassesTestMixin, CustomFormValidator, UpdateView):
    model = PrepCard
    form_class = PrepCardForm
    template_name = "prepcards/prepcard_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        context["formset"] = IngredientFormSet(IngredientUsed.objects.filter(card=prepcard.id))
        return context
    
    # Only creator can edit the card
    def test_func(self):
        obj = self.get_object()
        return obj.created_by  == self.request.user

class PrepDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PrepCard
    template_name = "prepcards/prepcard_delete.html"
    success_url = reverse_lazy("prepcard_list")
    
    # Only creator can delete the card
    def test_func(self):
        obj = self.get_object()
        return obj.created_by  == self.request.user

def serve_ingredient_form(request):
    form = IngredientFormSet()
    context = {
        "extra_form":form
    }
    return render(request, "partials/prepcards/ingredient_form.html", context)