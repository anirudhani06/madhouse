from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, FriendRequest

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


@receiver(m2m_changed, sender=Profile.friends.through)
def friend_request(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        user = Profile.objects.filter(id=instance.id).first()
        receiver = Profile.objects.filter(id__in=kwargs.get("pk_set")).first()
        FriendRequest.objects.create(sender=user, receiver=receiver)

    if action == "post_remove":
        user = Profile.objects.filter(id=instance.id).first()
        receiver = Profile.objects.filter(id__in=kwargs.get("pk_set")).first()
        FriendRequest.objects.create(
            sender=user, receiver=receiver, msg="removed you from friend list"
        )
