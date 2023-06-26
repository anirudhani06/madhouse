from django.urls import path
from . import views

urlpatterns = [
    path("", views.people, name="people"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
]
