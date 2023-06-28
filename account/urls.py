from django.urls import path
from . import views

urlpatterns = [
    path("", views.people, name="people"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("user_profile/<str:username>/", views.user_profile, name="user_profile"),
    path("settings/", views.settings, name="settings"),
    path("favourite/", views.favourite, name="favourite"),
    path("notifications/", views.notifications, name="notifications"),
    path("add_friend/", views.add_friend, name="add_friend"),
]
