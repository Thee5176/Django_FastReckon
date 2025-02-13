from django.urls import path

from .views import BalanceSheetView, IncomeView, CashFlowView, FinancialIndexView

urlpatterns = [
    path("balance-sheet/", BalanceSheetView.as_view(), name="balance-sheet"),
    path("income-statement/", IncomeView.as_view(), name="income-statement"),
    path("cashflow-statement/", CashFlowView.as_view(), name="cashflow-statement"),
    path("financial-index/", FinancialIndexView.as_view(), name="financial-index"),
]
