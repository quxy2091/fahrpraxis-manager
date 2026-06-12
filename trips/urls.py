from django.urls import path

from .views import (
    create_trip,
    trip_list,
    edit_trip,
    delete_trip,
)

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