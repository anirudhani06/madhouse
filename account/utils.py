from .models import Profile
from django.db.models import Q


def search_users(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    users = Profile.objects.filter(
        Q(username__startswith=q) | Q(name__startswith=q)
    ).exclude(user=request.user)
    return users
