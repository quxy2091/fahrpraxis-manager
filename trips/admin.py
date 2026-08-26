from django.contrib import admin

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "date",
        "user_profile",
        "traffic_type",
        "train_number",
        "from_station",
        "to_station",
        "vehicle",
        "hours",
    )

    list_filter = (
        "traffic_type",
        "shunting_type",
        "date",
        "vehicle",
    )

    search_fields = (
        "user_profile__user__username",
        "user_profile__user__first_name",
        "user_profile__user__last_name",
        "train_number",
        "from_station__name",
        "to_station__name",
    )

    ordering = (
        "-date",
        "-created_at",
    )