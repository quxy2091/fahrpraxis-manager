from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from employees.models import Employee


admin.site.unregister(User)


@admin.register(User)
class SemitaUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )

    fieldsets = (
        (
            "Benutzer",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            }
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            }
        ),
    )

    add_fieldsets = (
        (
            "Benutzer",
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            }
        ),
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change,
    ):

        super().save_model(
            request,
            obj,
            form,
            change,
        )