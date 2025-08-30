from django.urls import path
from .views import CustomLoginView

from . import views

urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(redirect_authenticated_user=True),
        name="accounts-login",
    ),
    path("logout/", views.logout_view, name="accounts-logout"),
    path("register/", views.register, name="accounts-register"),
]
