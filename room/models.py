from django.db import models
from account.models import Profile

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(blank=True, max_length=60, unique=True)
    coverpic = models.ImageField(upload_to="rooms/", default="default/room.jpg")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="rooms"
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="rooms")
    members = models.ManyToManyField(Profile, related_name="members", blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_cover_pic(self):
        if self.coverpic.url:
            return self.coverpic.url
        else:
            return ""

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["-updated_at"]


class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
