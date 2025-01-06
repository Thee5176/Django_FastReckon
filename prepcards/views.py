from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UserPassesTestMixin, 
)
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, FormView, DeleteView

from .mixins import CustomFormValidator
from .models import PrepCard, IngredientUsed
from .forms import PrepCardForm, IngredientFormSet

class PrepListView(LoginRequiredMixin, ListView):
    model = PrepCard
    template_name = "prepcards/prepcard_list.html"
# TODO: turn template into calendar format
    
class PrepCreateView(LoginRequiredMixin, CustomFormValidator, FormView):
    form_class = PrepCardForm
    template_name = "prepcards/prepcard_alter_form.html"
    success_url = reverse_lazy("prepcard_list")    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Create"
        context["ingredient_formset"] = IngredientFormSet(queryset=IngredientUsed.objects.none())
        return context
    
    
class PrepUpdateView(LoginRequiredMixin, UserPassesTestMixin, CustomFormValidator, UpdateView):
    model = PrepCard
    form_class = PrepCardForm
    template_name = "prepcards/prepcard_alter_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_name"] = "Update"
        context["ingredient_formset"] = IngredientFormSet(IngredientUsed.objects.filter(card=prepcard.id))
        return context
    
    # Only creator can edit the card
    def test_func(self):
        obj = self.get_object()
        return obj.owner  == self.request.user

class PrepDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PrepCard
    template_name = "prepcards/prepcard_delete.html"
    success_url = reverse_lazy("prepcard_list")
    
    # Only creator can delete the card
    def test_func(self):
        obj = self.get_object()
        return obj.owner  == self.request.user