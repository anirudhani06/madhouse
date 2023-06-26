from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "name", "email"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "name",
        "avatar",
        "email",
    ]


# group unregistered
admin.site.unregister(Group)
