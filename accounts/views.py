from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import redirect


class SemitaLoginView(LoginView):

    template_name = "accounts/login.html"

    redirect_authenticated_user = True


def logout_view(request):

    logout(request)

    return redirect("/login/")


def setup_admin(request):

    if User.objects.filter(username="admin").exists():

        return HttpResponse(
            "Admin existiert bereits."
        )

    User.objects.create_superuser(
        username="admin",
        email="michel.schaub@semita-gmbh.ch",
        password="Admin2026!"
    )

    return HttpResponse(
        "Admin erstellt."
    )