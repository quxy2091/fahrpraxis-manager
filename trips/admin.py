from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "date",
        "employee",
        "train_number",
        "service_type",
        "vehicle",
        "hours",
        "etcs",
    )

    list_filter = (
        "service_type",
        "vehicle",
        "etcs",
    )

    search_fields = (
        "train_number",
    )