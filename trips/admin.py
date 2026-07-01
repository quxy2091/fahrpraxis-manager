from django.contrib import admin

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "date",
        "employee",
        "train_number",
        "from_station",
        "to_station",
        "vehicle",
        "hours",
    )

    list_filter = (
        "vehicle",
        "from_station",
        "to_station",
    )

    search_fields = (
        "train_number",
        "notes",
    )