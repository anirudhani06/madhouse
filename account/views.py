from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def user_login(request):
    return render(request, "user/login.html")


def user_logout(request):
    pass


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
