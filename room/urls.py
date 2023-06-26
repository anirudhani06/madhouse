from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/rooms/", views.search_rooms, name="search_rooms"),
    path("create_room/", views.create_room, name="create_room"),
    path("update_room/<str:room_name>/", views.update_room, name="update_room"),
]
