from django.conf import settings
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2)
    guideline = models.TextField(null=True, blank=True)
    currency_sign = models.CharField(max_length=1, blank=True)
    #Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name=("books"), 
        on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ["abbr"]
        verbose_name = ("Book")
        verbose_name_plural = ("Books")
        unique_together = ['abbr','created_by']

    @property
    def record_count(self):
        return self.transactions.all().count
    
    def __str__(self):
        return self.abbr