from django.contrib import admin

from .models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "x",
        "y",
        "active",
    )

    list_editable = (
        "x",
        "y",
        "active",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
    )