from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils.translation import gettext_lazy as _

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

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
