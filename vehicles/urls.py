from django.urls import path

from .views import (
    vehicle_list,
    vehicle_dashboard,
)

urlpatterns = [

    path(
        "",
        vehicle_list,
        name="vehicle_list"
    ),

    path(
        "<int:vehicle_id>/",
        vehicle_dashboard,
        name="vehicle_dashboard"
    ),

]