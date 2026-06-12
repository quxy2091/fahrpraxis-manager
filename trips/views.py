from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from employees.models import Employee

from .models import Trip
from .forms import TripForm


@login_required
def trip_list(request):

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return redirect("/")

    trips = Trip.objects.filter(
        employee=employee
    ).order_by("-date")

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips
        }
    )


@login_required
def create_trip(request):

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return redirect("/")

    if request.method == "POST":

        form = TripForm(
            request.POST
        )

        if form.is_valid():

            trip = form.save(
                commit=False
            )

            trip.employee = employee

            trip.save()

            return redirect(
                "/fahrten/"
            )

    else:

        form = TripForm()

    return render(
        request,
        "trips/create_trip.html",
        {
            "form": form
        }
    )


@login_required
def edit_trip(
    request,
    trip_id
):

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return redirect("/")

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        employee=employee
    )

    if request.method == "POST":

        form = TripForm(
            request.POST,
            instance=trip
        )

        if form.is_valid():

            form.save()

            return redirect(
                "/fahrten/"
            )

    else:

        form = TripForm(
            instance=trip
        )

    return render(
        request,
        "trips/edit_trip.html",
        {
            "form": form,
            "trip": trip
        }
    )


@login_required
def delete_trip(
    request,
    trip_id
):

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return redirect("/")

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        employee=employee
    )

    if request.method == "POST":

        trip.delete()

        return redirect(
            "/fahrten/"
        )

    return render(
        request,
        "trips/delete_trip.html",
        {
            "trip": trip
        }
    )