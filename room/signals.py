from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Room
from account.models import Profile


# @receiver(pre_save, sender=Room)
# def room_create(sender, instance, *args, **kwargs):
#     room = instance
#     room.members.add(room.owner.id)
#     room.save()
