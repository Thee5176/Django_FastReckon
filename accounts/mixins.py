from django.db.models import QuerySet

class UserOwnedQuerysetMixin:
    """
    A mixin to add filter to get only objects owned by the current user
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if isinstance(queryset, QuerySet):
            return queryset.filter(created_by=self.request.user)
        return queryset