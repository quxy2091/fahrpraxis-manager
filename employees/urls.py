from django.urls import path

from .views import (
    employee_list,
    employee_dashboard,
)


urlpatterns = [

    path(
        "",
        employee_list,
        name="employee_list"
    ),

    path(
        "<int:employee_id>/",
        employee_dashboard,
        name="employee_dashboard"
    ),

]