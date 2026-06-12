from django.urls import path

from .views import (
    SemitaLoginView,
    logout_view,
)


urlpatterns = [

    path(
        "login/",
        SemitaLoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        logout_view,
        name="logout"
    ),

]