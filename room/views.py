from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Category, Favourites
from .utils import search_filter
from .forms import RoomForm

# Create your views here.


@login_required(login_url="login")
def home(request):
    rooms = Room.objects.all()
    categories = Category.objects.all()
    favourites = Favourites.objects.filter(user=request.user.profile).values_list(
        "room", flat=True
    )
    room_count = rooms.count()

    context = {
        "categories": categories,
        "rooms": rooms,
        "favourites": favourites,
        "room_count": room_count,
    }
    return render(request, "room/home.html", context)


@login_required(login_url="login")
def search_rooms(request):
    rooms = search_filter(request)
    query = request.GET.get("q")
    categories = Category.objects.all()
    favourites = Favourites.objects.filter(user=request.user.profile)
    room_count = Room.objects.all().count()

    context = {
        "categories": categories,
        "rooms": rooms,
        "query": query,
        "favourites": favourites,
        "room_count": room_count,
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
        if image is not None:
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


@csrf_exempt
@login_required(login_url="login")
def delete_room(request):
    if request.method == "POST":
        id = request.POST.get("id")
        user = request.user.profile
        room = Room.objects.filter(id=int(id)).first()

        if room is None:
            return HttpResponse("Room dose not exists")

        if room.owner != user:
            return HttpResponse("You can not delete this room!")

        room.delete()
        return JsonResponse({"success": True})


@csrf_exempt
@login_required(login_url="login")
def favourites(request):
    user = request.user.profile
    categories = Category.objects.all()
    rooms = Favourites.objects.filter(user=user)
    room_count = Room.objects.all().count()

    if request.method == "POST":
        room = Room.objects.filter(id=int(request.POST.get("id"))).first()
        if room is not None:
            filtered_room = Favourites.objects.filter(
                user=request.user.profile, room=room
            ).first()
            fav = Favourites()
            if filtered_room is None:
                fav.user = user
                fav.room = room
                fav.save()
                return JsonResponse({"success": True})
            else:
                filtered_room.delete()
                return JsonResponse({"success": False})

    context = {"categories": categories, "rooms": rooms, "room_count": room_count}
    return render(request, "room/favourite.html", context)
