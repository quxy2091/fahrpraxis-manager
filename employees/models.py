from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    yearly_target_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1
    )

    def __str__(self):
        return self.name


class Employee(models.Model):

    ROLE_CHOICES = [
        ('employee', 'Mitarbeiter'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True
    )

    entry_date = models.DateField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    etcs_authorized = models.BooleanField(
        default=False
    )

    external_signal_authorized = models.BooleanField(
        default=False
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"