from datetime import date
from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from employees.models import Employee
from trips.models import Trip
from vehicles.models import Vehicle


@login_required
def startseite(request):

    planungen = []

    planungs_ordner = (
        Path(settings.BASE_DIR)
        / "documents"
        / "planungen"
    )

    if planungs_ordner.exists():

        for datei in sorted(
            planungs_ordner.glob("*.pdf"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        ):

            planungen.append({
                "name": datei.name,
                "url": f"/planungen/{datei.name}"
            })

    return render(
        request,
        "dashboard/startseite.html",
        {
            "planungen": planungen
        }
    )


@login_required
def home(request, year=None):

    base_year = date.today().year

    if year is None:
        current_year = base_year
    else:
        current_year = year

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    employees = Employee.objects.all()

    employee_stats = []

    for emp in employees:

        trips = Trip.objects.filter(
            employee=emp,
            date__year=current_year
        )

        total_hours = sum(
            trip.hours for trip in trips
        )

        target_hours = emp.category.yearly_target_hours

        percent = 0

        if target_hours > 0:
            percent = round(
                (total_hours / target_hours) * 100,
                1
            )

        employee_stats.append({
            "employee": emp,
            "total_hours": total_hours,
            "target_hours": target_hours,
            "percent": percent,
        })

    vehicle_refresh = []

    vehicles = Vehicle.objects.filter(
        active=True
    )

    for vehicle in vehicles:

        last_trip = Trip.objects.filter(
            vehicle=vehicle
        ).order_by("-date").first()

        if last_trip:

            days_since = (
                date.today() - last_trip.date
            ).days

            if days_since > 180:

                status = "Fällig"
                status_icon = "images/signal_faellig.PNG"

            elif days_since > 90:

                status = "Warnung"
                status_icon = "images/signal_warnung.PNG"

            else:

                status = "Aktuell"
                status_icon = "images/signal_ok.PNG"

            vehicle_refresh.append({
                "vehicle": vehicle,
                "last_trip": last_trip.date,
                "days_since": days_since,
                "status": status,
                "status_icon": status_icon,
            })

    if employee:

        trips = Trip.objects.filter(
            employee=employee,
            date__year=current_year
        ).order_by("-date")

        recent_trips = trips[:10]

        total_hours = sum(
            trip.hours for trip in trips
        )

        target_hours = employee.category.yearly_target_hours

        percent = 0

        if target_hours > 0:
            percent = round(
                (total_hours / target_hours) * 100,
                1
            )

        remaining = target_hours - total_hours

    else:

        recent_trips = []
        total_hours = 0
        target_hours = 0
        percent = 0
        remaining = 0

    return render(
        request,
        "dashboard/home.html",
        {
            "employee": employee,
            "base_year": base_year,
            "current_year": current_year,
            "total_hours": total_hours,
            "target_hours": target_hours,
            "percent": percent,
            "remaining": remaining,
            "recent_trips": recent_trips,
            "employee_stats": employee_stats,
            "vehicle_refresh": vehicle_refresh,
        }
    )