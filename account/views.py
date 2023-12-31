from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm, ProfileForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from room.models import Room, Category, Favourites
from .models import Profile, FriendRequest
from .utils import search_users

# Create your views here.


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "user/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@csrf_exempt
def user_register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.name.capitalize()
            user.save()
            return redirect("login")

    context = {"form": form}
    return render(request, "user/register.html", context)


@login_required(login_url="login")
def profile(request):
    user = request.user.profile
    rooms = Room.objects.select_related("owner").filter(owner=user)
    favourites = Favourites.objects.filter(user=user).values_list("room", flat=True)
    friend_list = user.friends.all()
    context = {
        "user": user,
        "rooms": rooms,
        "favourites": favourites,
        "friend_list": friend_list,
    }
    return render(request, "user/profile.html", context)


@csrf_exempt
@login_required(login_url="login")
def settings(request):
    form = ProfileForm(instance=request.user.profile)
    categories = Category.objects.all()
    room_count = Room.objects.all().count()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.name = profile.name.capitalize()
            profile.username = profile.username.lower()
            profile.save()
            return redirect("profile")

    context = {"form": form, "categories": categories, "room_count": room_count}
    return render(request, "user/settings.html", context)


@login_required(login_url="login")
def people(request):
    page = "USERS"
    categories = Category.objects.all()
    users = search_users(request)
    room_count = Room.objects.all().count()
    context = {
        "categories": categories,
        "users": users,
        "page": page,
        "room_count": room_count,
    }
    return render(request, "user/people.html", context)


@login_required(login_url="login")
def user_profile(request, username):
    user = Profile.objects.filter(username=username).first()

    if user is None:
        return HttpResponse("user dose not exists")

    if user == request.user.profile:
        return redirect("profile")

    rooms = Room.objects.select_related("owner").filter(owner=user)
    favourites = Favourites.objects.filter(user=request.user.profile).values_list(
        "room", flat=True
    )
    friends = request.user.profile.friends.all()
    friend_list = user.friends.all()
    context = {
        "user": user,
        "rooms": rooms,
        "favourites": favourites,
        "friends": friends,
        "friend_list": friend_list,
    }

    return render(request, "user/profile.html", context)


@csrf_exempt
@login_required(login_url="login")
def add_friend(request):
    user = request.user.profile
    friend = Profile.objects.filter(username=request.POST.get("username")).first()

    if friend is None:
        return HttpResponse("User dose not exists")

    if friend in user.friends.all():
        user.friends.remove(friend)
        user.save()
        friend.friends.remove(user)
        friend.save()

        friend_request = FriendRequest()
        friend_request.sender = user
        friend_request.receiver = friend
        friend_request.msg = "removed you from friend list"
        friend_request.save()
        friend.is_notify_read = True
        friend.save()

        return JsonResponse({"success": False})
    else:
        user.friends.add(friend)
        user.save()
        friend.friends.add(user)
        friend.save()
        friend_request = FriendRequest()
        friend_request.sender = user
        friend_request.receiver = friend

        friend_request.save()
        friend.is_notify_read = True
        friend.save()
        return JsonResponse({"success": True})
