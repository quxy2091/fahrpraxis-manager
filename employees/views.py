from datetime import date

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from .models import Employee

from trips.models import Trip


@login_required
def employee_list(request):

    current_employee = Employee.objects.filter(
        user=request.user
    ).first()

    if not current_employee:
        return redirect("/")

    if current_employee.role != "admin":
        return redirect("/")

    employees = Employee.objects.filter(
        active=True
    ).order_by(
        "last_name",
        "first_name"
    )

    return render(
        request,
        "employees/employee_list.html",
        {
            "employees": employees
        }
    )


@login_required
def employee_dashboard(
    request,
    employee_id
):

    current_employee = Employee.objects.filter(
        user=request.user
    ).first()

    if not current_employee:
        return redirect("/")

    if current_employee.role != "admin":
        return redirect("/")

    employee = get_object_or_404(
        Employee,
        pk=employee_id
    )

    current_year = date.today().year

    trips = Trip.objects.filter(
        employee=employee,
        date__year=current_year
    ).order_by("-date")

    total_hours = sum(
        trip.hours for trip in trips
    )

    target_hours = (
        employee.category.yearly_target_hours
    )

    percent = 0

    if target_hours > 0:

        percent = round(
            (total_hours / target_hours) * 100,
            1
        )

    return render(
        request,
        "employees/employee_dashboard.html",
        {
            "employee": employee,
            "current_year": current_year,
            "trips": trips,
            "total_hours": total_hours,
            "target_hours": target_hours,
            "percent": percent,
        }
    )