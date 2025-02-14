from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from acc_books.models import Book
from acc_codes.models import Account
from transactions.models import Transaction
from pprint import pprint
            
class AccountDataMixin:
    def __init__(self):
        """
        Data Model for balances 
        
        { account_type(str) : 
          balance(int),
          { "root_list" : 
            { root_account(object) : root_balance(int)},
        }
        """
        self.root_balances = {}
        self.balances = {
        'asset' : self.get_account_balances(1),
        'liability' : self.get_account_balances(2),
        'equity' : self.get_account_balances(3),
        'revenue' : self.get_account_balances(4),
        'expense' : self.get_account_balances(5),
        'gain' : self.get_account_balances(6),
        'loss' : self.get_account_balances(7),
        }
        print(self.balances)
    
    def get_root_account_balances(self, account, balance):
        """Keep balance record of each root account. Sub-process of get_account_balance.

        Args:
            account (object): account object instance
            balance (int): account's associated balance

        Returns:
            Dictionary: root account with current balance.(see Data Model in __init__)
        """            
        try:
            self.root_balances[str(account.root)] += balance
        except KeyError:
            #initialize with current balance
            self.root_balances.update({str(account.root) : balance})
        
        return self.root_balances
        
    def get_account_balances(self, account_type):
        """Search account by code and get balance for all sub account

        Args:
            account (int): search with account code

        Returns:
            total_balance(int): account balance
        """
        account = Account.objects.filter(book__abbr='JA')
        account_list = account.filter(code__startswith=str(account_type))
        
        self.root_balances = {} # reset for each account_type
        total_balance = 0
        
        for account in account_list:
            # find balance for each account and add up to total balance
            balance = account.get_account_balance()
            total_balance += balance
            
            # store balance by root account
            self.get_root_account_balances(account, balance)
                
        return {"balance" : total_balance, "root_list" : self.root_balances}  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.balances)
        return context
    
class BalanceSheetView(LoginRequiredMixin, AccountDataMixin, TemplateView):
    template_name = "reports/main/balance_sheet.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["net_income"] = context["revenue"]["balance"]-context["expense"]["balance"]
        context["other_gain_loss"] = context["gain"]["balance"]-context["loss"]["balance"]
        context["net_equity"] = context["equity"]["balance"] + context["net_income"] + context["other_gain_loss"]
        return context
    
class IncomeView(LoginRequiredMixin, AccountDataMixin, TemplateView):
    template_name = "reports/main/income_statement.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["net_income"] = context["revenue"]["balance"] - context["expense"]["balance"]
        return context
    
class CashFlowView(LoginRequiredMixin, AccountDataMixin, TemplateView):
    template_name = "reports/main/cashflow_statement.html"
    
class FinancialIndexView(LoginRequiredMixin, AccountDataMixin, TemplateView):
    template_name = "reports/financial_index.html"