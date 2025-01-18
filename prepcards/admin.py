from django.contrib import admin

from .models import PrepCard, IngredientUsed

class IngredientUsedInlineAdmin(admin.StackedInline):
    model = IngredientUsed
    
class PrepCardAdmin(admin.ModelAdmin):
    inlines = [IngredientUsedInlineAdmin]    


admin.site.register(PrepCard, PrepCardAdmin)
