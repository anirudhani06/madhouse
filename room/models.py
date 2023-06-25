from django.db import models
from account.models import Profile

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=40, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="rooms")
    members = models.ManyToManyField(Profile, related_name="members")
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
