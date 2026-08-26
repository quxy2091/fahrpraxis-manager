from django.urls import path

from .views import (
    employee_dashboard,
    employee_edit,
    employee_list,
    employee_year_pdf,
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

    path(
        "<int:employee_id>/jahr/<int:year>/",
        employee_dashboard,
        name="employee_dashboard_year"
    ),

    path(
        "<int:employee_id>/jahr/<int:year>/pdf/",
        employee_year_pdf,
        name="employee_year_pdf"
    ),

    path(
        "<int:employee_id>/bearbeiten/",
        employee_edit,
        name="employee_edit"
    ),

]