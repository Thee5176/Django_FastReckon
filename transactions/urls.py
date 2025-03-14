from django.urls import path
from .views import (
    TransactionListView, 
    TransactionDetailView, 
    TransactionCreateView, 
    TransactionUpdateView, 
    TransactionDeleteView,
    TransactionConfirmView,
    add_entry_form,
    filter_transaction_by_book,
)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("create/", TransactionCreateView.as_view(), name="transaction_create"),
    path("create/with-base/<slug:slug>", TransactionCreateView.as_view(), name="transaction_create"),
    path("<slug:slug>", TransactionDetailView.as_view(), name="transaction_detail"),
    path("<slug:slug>/confirm/", TransactionConfirmView.as_view(), name="transaction_confirm"),
    path("<slug:slug>/update/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("<slug:slug>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
    path("htmx/get_extra_entryform/", add_entry_form, name="get_extra_entryform"),
    path("htmx/get_transaction_table/", filter_transaction_by_book, name="get_transaction_table"),
]
