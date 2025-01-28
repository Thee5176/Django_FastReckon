from django.contrib import admin

from .models import RootAccount, Account

    
admin.site.register(RootAccount)
admin.site.register(Account)