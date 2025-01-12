from django.urls import path
from .views import IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
    path("create/", IngredientCreateView.as_view(), name="ingredient_create"),
    path("<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient_update"),
    path("<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),
]
