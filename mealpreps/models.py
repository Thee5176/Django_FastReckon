from django.conf import settings
from django.urls import reverse
from django.db import models

class PrepIngredient(models.Model):
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    # TODO: create price field
    # TODO: create slug field 'ingredient-000g'
    
class PrepCard(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    prep_duration = models.DurationField(null=True, blank=True)
    # ingredient = models.ForeignKey(PrepIngredient, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Card No. {self.pk}"
    
    def get_absolute_url(self):
        return reverse("mealprep_edit", kwargs={"pk": self.pk})
    
    # TODO: generator for running speific ID for each user