from django.db import models

class Ingredient(models.Model):

    INGREDIENT_CATAGORIES = (
        (1,"Vegetables"),
        (2,"Eggs"),
        (3,"Dairy Products"),
        (4,"Meat"),
        (5,"Seafoods"),
        (6,"Fats and Oils"),
        (7,"Spices and Herbs")
        (8,"Bread, Grains and Rices")
    )
    
    UNIT = (
        (1, "per 100 g"),
        (10, "per 1 kg"),
    )
    
    name = models.CharField(max_length=50)
    catagory = models.IntegerField(choices=INGREDIENT_CATAGORIES)
    unit = models.IntegerField(label="unit",choices=UNIT)
    cost_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    # nutritient = models.ForeignKey
    
    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")

    def get_price_per_100g(self):
        return self.cost_per_unit / self.unit
    
    def get_price_per_kg(self):
        return self.cost_per_unit * 10 / self.unit
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ingredient_detail", kwargs={"pk": self.pk})
