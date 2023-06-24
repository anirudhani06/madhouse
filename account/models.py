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

        return self.create_user(username, email, password, others)


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
    avatar = models.ImageField(upload_to="profile/", default="/media/default.jpg")
    email = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField("self", blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
