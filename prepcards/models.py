from django.conf import settings
from django.urls import reverse
from django.db import models
    
from ingredients.models import Ingredient

class PrepCard(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    
    def __str__(self):
        return f"Card No. {self.pk}"
    
    def get_absolute_url(self):
        return reverse("prepcard_edit", kwargs={"pk": self.pk})
    # TODO: generator for running speific ID for each user

class IngredientUsed(models.Model):
    name = models.ForeignKey(Ingredient, related_name=("usages"), on_delete=models.CASCADE)
    amount_of_unit = models.DecimalField(max_digits=5, decimal_places=2)
    card = models.ForeignKey(PrepCard, related_name=("ingredients"), on_delete=models.CASCADE)
    # TODO: create price field
    # TODO: create slug field 'ingredient-000g'