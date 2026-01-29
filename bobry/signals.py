from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Bobr, Obserwacja, Activity, Zeremie


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Bobr)
def bobr_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.user,
            activity_type='BOBR',
            bobr=instance
        )


@receiver(post_save, sender=Obserwacja)
def obserwacja_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.autor,
            activity_type='OBS',
            obserwacja=instance
        )


def activity_bobr_created(sender, instance, created, **kwargs):
    if created and instance.user:
        Activity.objects.create(
            user=instance.user,
            activity_type='BOBR',
            bobr=instance
        )


@receiver(post_save, sender=Obserwacja)
def activity_obserwacja_created(sender, instance, created, **kwargs):
    if created and instance.autor:
        Activity.objects.create(
            user=instance.autor,
            activity_type='OBS',
            obserwacja=instance
        )

@receiver(post_save, sender=Zeremie)
def zeremie_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.budowniczy.user,
            activity_type='ZER',
            zeremie=instance
        )