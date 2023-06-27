from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

USER = get_user_model()


class RegisterForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput({"placeholder": "Name"}))
    username = forms.CharField(widget=forms.TextInput({"placeholder": "Username"}))
    email = forms.CharField(widget=forms.EmailInput({"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput({"placeholder": "Password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "Confirm password"})
    )

    class Meta:
        model = USER
        fields = ("name", "username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput({"id": "image_input"}), required=False
    )
    name = forms.CharField(widget=forms.TextInput({"placeholder": "Name"}))
    username = forms.CharField(widget=forms.TextInput({"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "Email"}))
    bio = forms.CharField(
        widget=forms.Textarea({"placeholder": "Write about yourself"})
    )

    class Meta:
        model = Profile
        fields = ("avatar", "name", "username", "email", "bio")
