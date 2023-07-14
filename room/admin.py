from django.contrib import admin
from .models import Category, Room, Favourites

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "is_private"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Favourites)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ["room", "user"]
