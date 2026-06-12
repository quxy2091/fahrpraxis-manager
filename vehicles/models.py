from django.db import models


class Vehicle(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    refresh_interval_days = models.PositiveIntegerField(
        default=180
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name