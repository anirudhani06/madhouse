from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **others):
        if not username:
            raise ValueError(_("Username must be set"))
        if not email:
            raise ValueError(_("Email must be set"))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **others)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **others):
        others.setdefault("is_superuser", True)
        others.setdefault("is_staff", True)

        if others.get("is_superuser") is not True:
            raise ValueError(_("Admin should be set is_superuser is True"))
        if others.get("is_staff") is not True:
            raise ValueError(_("Admin should be set is_staff is True"))

        return self.create_user(username, email, password, **others)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=250, unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=40, unique=True)
    avatar = models.ImageField(upload_to="profile/", default="default/avatar.jpg")
    email = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField("self", blank=True)
    is_online = models.BooleanField(default=False)
    is_notify_read = models.BooleanField(default=False)

    def get_avatar(self):
        return self.avatar.url

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="friend_requests"
    )
    msg = models.TextField(max_length=20, blank=True, default="Added To Your Friend")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.receiver.username

    class Meta:
        verbose_name = "Friend Request"
        verbose_name_plural = "Friend Requests"
        ordering = ["-created_at"]
