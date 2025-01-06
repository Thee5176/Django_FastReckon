from django.urls import path

urlpatterns = [
    path("/", IngredietView.as_view(), name="ingredient_")
    path("create/", IngredietView.as_view(), name="ingredient_")
    path("<pk:pk>/delete/", IngredietView.as_view(), name="ingredient_")
    path("<pk:pk>/update/", IngredietView.as_view(), name="ingredient_")
]
