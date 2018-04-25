"""Managers for objects."""

from django.db import models
from django.utils.timezone import now


class PreventDeletionQuerySet(models.query.QuerySet):
    """QuerySet whose delete() does not delete items.

    But instead marks the rows as archived, and updates the timestamps.
    """

    def delete(self):
        """Set the deleted_at field."""
        deleted_at = now()
        self.update(deleted_at=deleted_at)

    def restore(self):
        """Update the object to have no deleted_at value."""
        self.update(deleted_at=None)

    def all(self):
        """Fetch all active items."""
        return self.filter(deleted_at__isnull=True)


class PreserveModelManager(models.Manager):
    """Manager returns a PreventDeletionQuerySet query set."""

    def get_query_set(self):
        """Default query set changed."""
        return PreventDeletionQuerySet(self.model, using=self._db)

    def restore(self):
        """Restore a soft deletion / archive."""
        return self.get_query_set().restore()
