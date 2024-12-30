from django.urls import path

from .views import PrepListView, PrepUpdateView, PrepCreateView, PrepDeleteView

urlpatterns = [
    path("", PrepListView.as_view(), name="mealprep_list"),
    path("create/", PrepCreateView.as_view(), name="mealprep_create"),
    path("<int:pk>/", PrepUpdateView.as_view(), name="mealprep_edit"),
    path("delete/<int:pk>/", PrepDeleteView.as_view(), name="mealprep_delete"),
]
