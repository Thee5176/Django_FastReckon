from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .management.commands.populate_account import AccountPopulator

User = get_user_model()

@staticmethod
@receiver(post_save, sender=User)
def handle_post_migrate(sender, created, instance,**kwargs):
    if created:
        AccountPopulator.populate_root()
        print(f"populated root account")
        AccountPopulator.populate_base(user_instance=instance)
        print(f"populated initial account structure for new user: {instance.username}")