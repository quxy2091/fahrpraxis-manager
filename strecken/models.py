from django.db import models

from stations.models import Station
from employees.models import Employee


class Route(models.Model):

    number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Streckennummer"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Bezeichnung"
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:

        ordering = [
            "number"
        ]

        verbose_name = "Strecke"
        verbose_name_plural = "Strecken"

    def __str__(self):

        return f"{self.number} - {self.name}"


class RouteStation(models.Model):

    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="stations"
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
    )

    position = models.PositiveIntegerField()

    kilometer = models.DecimalField(
        max_digits=7,
        decimal_places=3,
        null=True,
        blank=True
    )

    class Meta:

        ordering = [
            "route",
            "position"
        ]

        unique_together = (
            "route",
            "position"
        )

        verbose_name = "Betriebspunkt auf Strecke"
        verbose_name_plural = "Betriebspunkte auf Strecken"

    def __str__(self):

        return (
            f"{self.route.number} | "
            f"{self.position} | "
            f"{self.station}"
        )


class EmployeeRoute(models.Model):

    STATUS_CHOICES = [

        ("ausbildung", "In Ausbildung"),
        ("kundig", "Kundig"),
        ("abgelaufen", "Abgelaufen"),

    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="routes"
    )

    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="employees"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="kundig"
    )

    valid_until = models.DateField(
        null=True,
        blank=True
    )

    last_trip = models.DateField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:

        unique_together = (
            "employee",
            "route"
        )

        ordering = [
            "employee",
            "route"
        ]

        verbose_name = "Streckenkundigkeit"
        verbose_name_plural = "Streckenkundigkeiten"

    def __str__(self):

        return f"{self.employee} - {self.route}"