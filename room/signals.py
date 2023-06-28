from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Room
from account.models import Profile
from django.template.defaultfilters import slugify


@receiver(pre_save, sender=Room)
def room_create_slug(sender, instance, *args, **kwargs):
    room = instance
    room.slug = slugify(room.name)


@receiver(post_save, sender=Room)
def room_create(sender, instance, created, *args, **kwargs):
    room = instance
    if created:
        room.members.add(room.owner)
        room.save()
