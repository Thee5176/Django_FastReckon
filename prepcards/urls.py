from django.urls import path

from .views import PrepListView, PrepUpdateView, PrepCreateView, PrepDeleteView
from .views import serve_ingredient_form

urlpatterns = [
    path("", PrepListView.as_view(), name="prepcard_list"),
    path("create/", PrepCreateView.as_view(), name="prepcard_create"),
    path("<int:pk>/update/", PrepUpdateView.as_view(), name="prepcard_edit"),
    path("<int:pk>/delete/", PrepDeleteView.as_view(), name="prepcard_delete"),
    path("htmx/serve-ingredient-form/", serve_ingredient_form , name='serve-ingredient-form'),
]
