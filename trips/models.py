from django.db import models

from employees.models import Employee
from vehicles.models import Vehicle


class Trip(models.Model):

    SERVICE_CHOICES = [
        ('zug', 'Zug'),
        ('rads', 'RadS'),
        ('rabe', 'RaBe'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    train_number = models.CharField(
        max_length=50
    )

    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT
    )

    etcs = models.BooleanField(
        default=False
    )

    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.date} - {self.train_number}"