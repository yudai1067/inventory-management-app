from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            body = request.POST
            User.objects.create_user(
                username=body.get("username"),
                password=body.get("password"),
            )
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            login(request, user)
            return redirect("inventory-index")
    else:
        form = UserForm(
            initial={
                "username": "",
                "password": "",
            }
        )
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts-login")
