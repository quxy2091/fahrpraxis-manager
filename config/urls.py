from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import SemitaLoginView


urlpatterns = [

    path(
        "login/",
        SemitaLoginView.as_view(),
        name="login"
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

] + static(
    "planungen/",
    document_root=settings.BASE_DIR / "documents" / "planungen"
)