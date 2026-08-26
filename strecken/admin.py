from django.contrib import admin

from .models import Route
from .models import RouteStation
from .models import EmployeeRoute


class RouteStationInline(admin.TabularInline):

    model = RouteStation
    extra = 0
    ordering = ["position"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):

    list_display = (
        "number",
        "name",
        "active",
    )

    search_fields = (
        "number",
        "name",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "number",
    )

    inlines = [
        RouteStationInline
    ]


@admin.register(EmployeeRoute)
class EmployeeRouteAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "route",
        "status",
        "valid_until",
        "last_trip",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "route__name",
    )