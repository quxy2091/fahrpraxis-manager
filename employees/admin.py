from django.contrib import admin
from .models import Category, Employee


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "yearly_target_hours",
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "user",
        "category",
        "role",
        "active",
    )

    fields = (
        "user",
        "first_name",
        "last_name",
        "email",
        "entry_date",
        "category",
        "etcs_authorized",
        "external_signal_authorized",
        "role",
        "active",
    )

    list_filter = (
        "category",
        "role",
        "active",
    )

    search_fields = (
        "first_name",
        "last_name",
    )