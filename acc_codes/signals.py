from django.db.models.signals import post_save
from django.dispatch import receiver

from acc_books.models import Book
from .management.commands.populate_account import AccountPopulator

@staticmethod
@receiver(post_save, sender=Book)
def handle_post_migrate(sender, created, instance, user=None, **kwargs):
    if created:
        # Let the book create if can populate account
        try:
            book = instance
            user = instance.created_by
            print(f"Book:{book},User:{user}")
            AccountPopulator.populate_base(book_instance=book,user_instance=user)
            print(f"populated initial account structure for user: {user.username} on book: {book.name}")

        # Delete Book if account can't be populated
        except Exception as e:
            instance.delete()
            print(f"Error: Not allow creating book without initial account with error {e}")