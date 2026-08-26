from django.urls import path

from .views import create_trip
from .views import delete_trip
from .views import edit_trip
from .views import trip_list
from .views import trip_pdf


urlpatterns = [

    path(
        "",
        trip_list,
        name="trip_list"
    ),

    path(
        "neu/",
        create_trip,
        name="create_trip"
    ),

    path(
        "pdf/",
        trip_pdf,
        name="trip_pdf"
    ),

    path(
        "<int:trip_id>/bearbeiten/",
        edit_trip,
        name="edit_trip"
    ),

    path(
        "<int:trip_id>/loeschen/",
        delete_trip,
        name="delete_trip"
    ),

]