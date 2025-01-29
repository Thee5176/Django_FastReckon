from django.urls import path
from .views import (
    AccountListView, 
    AccountDetailView, 
    AccountCreateView, 
    AccountUpdateView, 
    AccountDeleteView,
    filter_account_by_book,
)

urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("create/", AccountCreateView.as_view(), name="account_create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/update/", AccountUpdateView.as_view(), name="account_update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path("htmx/get_account_table/", filter_account_by_book, name="get_account_table"),
]