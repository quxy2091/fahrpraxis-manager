from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "uploaded_at",
        "active",
    )

    list_filter = (
        "category",
        "active",
    )

    search_fields = (
        "title",
    )