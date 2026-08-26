from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

import json

from stations.models import Station


@login_required
def map_view(request):

    return render(
        request,
        "kundigkeit/map.html",
        {
            "page_title": "Kundigkeit",
        },
    )


@login_required
def editor_view(request):

    stations = Station.objects.order_by(
        "name"
    )

    return render(
        request,
        "kundigkeit/editor.html",
        {
            "stations": stations,
        },
    )


@login_required
def stations_json(request):

    data = []

    for station in Station.objects.order_by("name"):

        data.append({

            "id": station.id,
            "name": station.name,
            "x": station.x,
            "y": station.y,

        })

    return JsonResponse(
        data,
        safe=False
    )


@login_required
@require_POST
def save_position(request):

    data = json.loads(
        request.body
    )

    station = Station.objects.get(
        pk=data["id"]
    )

    station.x = data["x"]
    station.y = data["y"]

    station.save()

    return JsonResponse({

        "success": True

    })