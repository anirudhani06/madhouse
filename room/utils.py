from .models import Room, Category
from django.db.models import Q


def search_filter(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""

    rooms = Room.objects.filter(Q(name__startswith=q) | Q(category__name__startswith=q))

    return rooms
