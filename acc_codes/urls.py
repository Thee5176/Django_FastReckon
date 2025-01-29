from django.urls import path

from .views import AccountListView, AccountDetailView, AccountCreateView, AccountUpdateView, AccountDeleteView

urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("create/", AccountCreateView.as_view(), name="account_create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/update/", AccountUpdateView.as_view(), name="account_update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
]