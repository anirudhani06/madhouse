from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from account.models import Profile


# Create your views here.
@login_required(login_url="login")
def chat(request, username):
    user = Profile.objects.filter(username=username).first()
    friends = user.friends.all()

    if user is None:
        return HttpResponse("User not found")
    context = {"user": user, "friend_list": friends}
    return render(request, "chat/chat.html", context)
