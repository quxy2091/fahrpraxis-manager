from .models import Employee


def employee_context(request):

    employee = None

    if request.user.is_authenticated:

        employee = Employee.objects.filter(
            user=request.user
        ).first()

    return {
        "employee": employee
    }