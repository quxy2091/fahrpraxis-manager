from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.startseite,
        name="startseite"
    ),

    path(
        "mein-cockpit/",
        views.home,
        name="home"
    ),

    path(
        "mein-cockpit/jahr/<int:year>/",
        views.home,
        name="year_home"
    ),

]