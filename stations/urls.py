from django.urls import path

from . import views

app_name = "kundigkeit"

urlpatterns = [

    path(
        "",
        views.map_view,
        name="map",
    ),

    path(
        "editor/",
        views.editor_view,
        name="editor",
    ),

    path(
        "stations/",
        views.stations_json,
        name="stations",
    ),

    path(
        "save-position/",
        views.save_position,
        name="save_position",
    ),

]