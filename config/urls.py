from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import SemitaLoginView
from accounts.views import setup_admin


urlpatterns = [

    path(
        "login/",
        SemitaLoginView.as_view(),
        name="login"
    ),

    path(
        "setup-admin/",
        setup_admin,
        name="setup_admin"
    ),

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("dashboard.urls")
    ),

    path(
        "fahrten/",
        include("trips.urls")
    ),

    path(
        "mitarbeiter/",
        include("employees.urls")
    ),

    path(
        "fahrzeuge/",
        include("vehicles.urls")
    ),

    path(
        "accounts/",
        include("accounts.urls")
    ),

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