from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import pandas as pd
import os, sys
from acc_codes.models import Account, RootAccount

class AccountPopulator:
    # Prepare file path
    root_path = os.path.join(settings.STATIC_ROOT, "csv/root.csv")
    base_path = os.path.join(settings.STATIC_ROOT, "csv/base.csv")
    
    if not all([root_path, base_path]):
        raise FileNotFoundError("One or more static files are missing!")
    
    # Read CSV file into DataFrame
    df_root = pd.read_csv(root_path, delimiter=";", quotechar='"')
    df_base = pd.read_csv(base_path, delimiter=";", quotechar='"')

    # Adjust nan value to None
    df_base['balance'] = df_base['balance'].replace({pd.NA:None})
    
    def csv_to_variable(df):
        """_summary_

        Args:
            df (File handler): dataframe handler
        """
        def decorator(func):
            def wrapper_func(*args, **kwargs):       
                for _, row in df.iterrows():
                    c=str(row['code'])
                    n=row['name']
                    b=row['balance']
                    g=row['guideline']
                    func(c,n,b,g, *args, **kwargs)
            return wrapper_func
        return decorator

    @csv_to_variable(df_root)      
    def populate_root(c,n,b,g):
        try:
            root_account = RootAccount.objects.filter(code=c).first()
            if root_account:
                pass
                # Do Nothing and Update CSV with existing account
            else:
                # Import account from CSV
                root_account = RootAccount(
                    code=c,
                    name=n,
                    guideline=g,
                    balance=b,
                )
            # Save account, trigger the custom save() method     
            root_account.save()
                
        except Exception as e:
            print(f"Encounter error when creating account: {c} with error {e}")
            sys.exit(1)

    @csv_to_variable(df_base)
    def populate_base(c,n,b,g,book_instance=None,user_instance=None):
        if not book_instance == None:
            if not user_instance == None:
                # Check if root_account exist
                root_code = int(c[:4])        
                try:
                    root_instance = RootAccount.objects.get(code=root_code)
                except RootAccount.DoesNotExist:
                    print(f"Account with code {root_code} does not exist.")
                    sys.exit(1)
                
                # Check if account for the book is exist
                try:
                    account = Account.objects.get(code=c,book=book_instance)
                    # Do Nothing CSV with existing account
                    pass
                    print(f"Skip without makeing change on {account.code}")
                    
                except Account.DoesNotExist:
                    # Import account from CSV
                    account = Account(
                        book=book_instance,
                        root=root_instance,     #code 1/2
                        sub_account=c[-2:],         #code 2/2
                        name=n,
                        guideline=g,
                        balance=b,
                        created_by=user_instance
                    )
                    # Save account, trigger the custom save() method     
                    account.save()
                    print(f"Succesfully create account: {account}")
                
                except Exception as e:
                    print(f"Encounter error creating account: {c} with error {e}")
                    sys.exit(1)
                    
            else:
                print(f"Base Account isn't created: no book_instance is parsed.")
                sys.exit(1)
               
        else:
            print(f"Base Account isn't created: no user_instance is parsed.")
            sys.exit(1)

class Command(BaseCommand):
    help = "This command populate account level 1-3 and assign basic account to new user"
    
    def handle(self, *args, **kwargs):
        print("Running script populate_account...")
        AccountPopulator.populate_root()
        print("Succesfully populated root account")
    