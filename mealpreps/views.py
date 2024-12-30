from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UserPassesTestMixin, 
)
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .models import PrepCard
    
class PrepCreateView(LoginRequiredMixin, CreateView):
    model = PrepCard
    template_name = "mealpreps/mealprep_create.html"
    fields = ("date","prep_duration")
    
    # Auto add owner field
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PrepListView(LoginRequiredMixin, ListView):
    model = PrepCard
    template_name = "mealpreps/mealprep_list.html"
# TODO: turn template into calendar format
    
class PrepUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PrepCard
    template_name = "mealpreps/mealprep_create.html"
    fields = ("date","prep_duration")
    
    # Only creator can edit the card
    def test_func(self):
        obj = self.get_object()
        return obj.owner  == self.request.user
    
    # Auto add owner field
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PrepDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PrepCard
    template_name = "mealpreps/mealprep_delete.html"
    success_url = reverse_lazy("mealprep_list")
    
    # Only creator can delete the card
    def test_func(self):
        obj = self.get_object()
        return obj.owner  == self.request.user