from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Category
from .utils import search_filter
from .forms import RoomForm

# Create your views here.


@login_required(login_url="login")
def home(request):
    rooms = Room.objects.all()
    categories = Category.objects.all()
    favourites = request.user.profile.favourites.all()

    context = {"categories": categories, "rooms": rooms, "favourites": favourites}
    return render(request, "room/home.html", context)


@login_required(login_url="login")
def search_rooms(request):
    rooms = search_filter(request)
    query = request.GET.get("q")
    categories = Category.objects.all()
    favourites = request.user.profile.favourites.all()

    context = {
        "categories": categories,
        "rooms": rooms,
        "query": query,
        "favourites": favourites,
    }
    return render(request, "room/search.html", context)


@csrf_exempt
@login_required(login_url="login")
def create_room(request):
    categories = Category.objects.all()
    form = RoomForm()
    if request.method == "POST":
        image = request.FILES.get("coverpic")
        name = request.POST.get("name")
        category_name = request.POST.get("category")
        is_private = True if request.POST.get("is_private") is not None else False
        category, _ = Category.objects.get_or_create(name=category_name)

        room = Room()
        room.owner = request.user.profile
        room.name = name
        room.category = category
        room.coverpic = image
        room.is_private = is_private
        room.save()
        return redirect("home")
    context = {"categories": categories, "form": form}
    return render(request, "room/create_room.html", context)


@csrf_exempt
@login_required(login_url="login")
def update_room(request, room_name):
    user = request.user.profile
    categories = Category.objects.all()
    room = Room.objects.filter(name=room_name).first()
    if room is None:
        return HttpResponse("Invalid room name.")
    if room.owner != user:
        return HttpResponse("You cannot update this room.")

    if request.method == "POST":
        category_name = request.POST.get("category")
        category, _ = Category.objects.get_or_create(name=category_name)
        room.coverpic = (
            request.FILES.get("coverpic")
            if request.FILES.get("coverpic") is not None
            else room.coverpic
        )
        room.category = category
        room.name = request.POST.get("name")
        room.is_private = True if request.POST.get("is_private") is not None else False
        room.save()
        return redirect("home")

    context = {"categories": categories, "room": room}
    return render(request, "room/update_room.html", context)
