from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .management.commands.populate_account import AccountPopulator

# @staticmethod
# @receiver(post_save, sender=Book)
# def handle_post_migrate(sender, created, instance, user=None, **kwargs):
#     if created and user:
#         AccountPopulator.populate_base(book=instance,user=user_instance)
#         print(f"populated initial account structure for user: {user.username} on book: {book.name}")