from datetime import date

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from employees.models import Employee

from .models import Vehicle

from trips.models import Trip


@login_required
def vehicle_list(request):

    current_employee = Employee.objects.filter(
        user=request.user
    ).first()

    if not current_employee:
        return redirect("/")

    if current_employee.role != "admin":
        return redirect("/")

    vehicles = Vehicle.objects.filter(
        active=True
    ).order_by(
        "name"
    )

    return render(
        request,
        "vehicles/vehicle_list.html",
        {
            "vehicles": vehicles
        }
    )


@login_required
def vehicle_dashboard(
    request,
    vehicle_id
):

    current_employee = Employee.objects.filter(
        user=request.user
    ).first()

    if not current_employee:
        return redirect("/")

    if current_employee.role != "admin":
        return redirect("/")

    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id
    )

    trips = Trip.objects.filter(
        vehicle=vehicle
    ).order_by(
        "-date"
    )

    last_trip = trips.first()

    total_hours = sum(
        trip.hours for trip in trips
    )

    current_year = date.today().year

    yearly_trips = trips.filter(
        date__year=current_year
    )

    yearly_hours = sum(
        trip.hours for trip in yearly_trips
    )

    return render(
        request,
        "vehicles/vehicle_dashboard.html",
        {
            "vehicle": vehicle,
            "trips": trips[:20],
            "last_trip": last_trip,
            "yearly_hours": yearly_hours,
            "yearly_count": yearly_trips.count(),
        }
    )