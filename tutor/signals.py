"""
File for receiver functions.
You can read more about what those are here:
https://docs.djangoproject.com/en/1.11/topics/signals/
"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
import tutor.models as models


@receiver(post_delete, sender=models.Subject)
def delete_category(sender, **kwargs):
    """
    deletes the category that has a one-to-one relationship with
    a given subject when deleting that subject
    """
    sub = kwargs.get("instance")
    if sub.category:
        sub.category.delete()
