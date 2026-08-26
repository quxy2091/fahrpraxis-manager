from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import SemitaLoginView
from accounts.views import setup_admin
from accounts.views import logout_view


urlpatterns = [

    # Login
    path(
        "login/",
        SemitaLoginView.as_view(),
        name="login"
    ),

    # Logout
    path(
        "logout/",
        logout_view,
        name="logout"
    ),

    # Passwort zurücksetzen
    path(
        "passwort/",
        include("django.contrib.auth.urls")
    ),

    # Einmaliges Admin-Setup
    path(
        "setup-admin/",
        setup_admin,
        name="setup_admin"
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Dashboard
    path(
        "",
        include("dashboard.urls")
    ),

    # Fahrten
    path(
        "fahrten/",
        include("trips.urls")
    ),

    # Mitarbeiter
    path(
        "mitarbeiter/",
        include("employees.urls")
    ),

    # Fahrzeuge
    path(
        "fahrzeuge/",
        include("vehicles.urls")
    ),

    # Stationen
    path(
        "stations/",
        include("stations.urls")
    ),

    # Accounts
    path(
        "accounts/",
        include("accounts.urls")
    ),

    # Kundigkeit
    path(
        "kundigkeit/",
        include("kundigkeit.urls")
    ),

] + static(
    "planungen/",
    document_root=settings.BASE_DIR / "documents" / "planungen"
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)