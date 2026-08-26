from django.db import models

from accounts.models import UserProfile
from vehicles.models import Vehicle
from stations.models import Station


class Trip(models.Model):

    TRAFFIC_CHOICES = [
        ("zug", "Zug"),
        ("rangieren", "Rangierbewegung"),
    ]

    SHUNTING_CHOICES = [
        ("direkt", "Direkt"),
        ("indirekt", "Indirekt"),
    ]

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="trips"
    )

    date = models.DateField()

    traffic_type = models.CharField(
        max_length=20,
        choices=TRAFFIC_CHOICES,
        default="zug"
    )

    shunting_type = models.CharField(
        max_length=20,
        choices=SHUNTING_CHOICES,
        blank=True
    )

    train_number = models.CharField(
        max_length=6,
        blank=True
    )

    from_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="departures"
    )

    to_station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="arrivals",
        blank=True,
        null=True
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        blank=True,
        null=True
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

        nummer = self.train_number or "Rangierbewegung"

        if self.to_station:
            strecke = f"{self.from_station} - {self.to_station}"
        else:
            strecke = f"{self.from_station}"

        return (
            f"{self.date} | "
            f"{nummer} | "
            f"{strecke}"
        )