from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

USER = get_user_model()


@receiver(post_save, sender=USER)
def create_profile(sender, instance, created, *args, **kwargs):
    profile = Profile()

    if created:
        profile.user = instance
        profile.username = instance.username
        profile.name = instance.name
        profile.email = instance.email
        profile.save()


@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, *args, **kwargs):
    user = USER.objects.filter(username=instance.username).first()

    if user is not None:
        if not created:
            user.username = instance.username
            user.name = instance.name
            user.email = instance.email
            user.save()
        else:
            pass
    else:
        pass
