from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import datetime
class RootAccount(models.Model):
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    
    code = models.IntegerField(
        primary_key=True, 
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(1000)
        ]
    )
    name = models.CharField(max_length=50)
    guideline = models.TextField(null=True, blank=True)
    balance = models.IntegerField(choices=BALANCE_TYPE)

    class Meta:
        ordering = ["code"]
        verbose_name = ("RootAccount")
        verbose_name_plural = ("RootAccounts")

    def __str__(self):
        return f"{self.code} | {self.name}"
    
    @property
    def get_type(self, as_str=False):
        TYPE_NAME = [
            "Asset",
            "Liability",
            "Equity",
            "Revenue",
            "Expense",
            "Gain",
            "Loss",
        ]
        
        code = int(str(self.code)[0])

        if as_str == True:
            return TYPE_NAME[code - 1]
        else:
            return code
    
    @property
    def get_group(self, as_str=False):
        GROUP_NAME = {
            11 : "Current Asset",
            12 : "Fixed Asset",
            21 : "Current Liability",
            22 : "Long-term Liability",
            30 : "Equity",
            41 : "Personal Revenue",
            42 : "Corporate Revenue",
            51 : "Personal Expense",
            52 : "Corporate Expense",
            61 : "Operation Gain",
            62 : "Non-operation Gain",
            71 : "Operation Loss",
            72 : "Non-operation Loss",
        }
        
        code = int(str(self.code)[:2])
        
        if as_str == True:
            return GROUP_NAME[code - 1]
        else:
            return code
    
class Account(models.Model):
    BALANCE_TYPE = [
        (1, "Dr"),
        (2, "Cr"),
    ]
    
    book = models.ForeignKey("acc_books.Book", related_name="accounts", on_delete=models.CASCADE)
    root = models.ForeignKey(RootAccount, related_name="accounts", on_delete=models.CASCADE)
    sub_account = models.CharField(max_length=2)
    detailed_account = models.CharField(max_length=2, null=True, blank=True)
    code = models.CharField(max_length=9, blank=True)
    name = models.CharField(max_length=50)
    balance = models.IntegerField(choices=BALANCE_TYPE, null=True, blank=True)
    guideline = models.TextField(null=True, blank=True)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #Meta
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=("accounts"), on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["root","sub_account","detailed_account"]
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")
    
    def update_code(self):
        self.code = f"{self.root.code}{self.sub_account}"
        if self.detailed_account :
            self.code += f"-{self.detailed_account}"
            
    def save(self,*args, **kwargs):
        self.update_code()
        super(Account, self).save(*args, **kwargs)
    
    def record_count(self):
        if self.entries.all():
            return len(self.entries.all())

    def get_account_type(self):
        return self.balance if self.balance else self.root.balance
    
    def get_account_balance(self):
        balance = 0
        for entry in self.entries.all():
            if entry.entry_type == self.get_account_type():
                balance += entry.amount
            else:
                balance -= entry.amount
        return balance
    
    def get_accumulated_budget(self):
        if self.monthly_budget:
            current_month = datetime.now().month
            return self.monthly_budget * current_month
    
    def get_bs_color_code(self):
        color_by_code = {
            0:"dark",
            1:"primary",
            2:"success",
            3:"danger",
            4:"warning",
            5:"info",
            6:"secondary",
            7:"secondary",
        }
        
        index = int(self.code[0])
        try:
            color = color_by_code[index]
            return color 
        except:
            print(f"Error: No color assigned to code {code}")
    
    def __str__(self):
        return f"{self.book} | {self.code} | {self.name}"
    
    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"pk": self.pk})
    