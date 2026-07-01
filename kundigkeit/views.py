from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def map_view(request):
    return render(
        request,
        "kundigkeit/map.html",
        {
            "page_title": "Kundigkeit",
        },
    )