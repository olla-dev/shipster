from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Vessel

@receiver(post_save, sender=Vessel)
def save_vessel(sender, instance, **kwargs):
    print("vessel updated.")

