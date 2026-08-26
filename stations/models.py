from django.db import models


class Station(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    active = models.BooleanField(
        default=True
    )

    x = models.FloatField(
        null=True,
        blank=True,
        verbose_name="X-Koordinate"
    )

    y = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Y-Koordinate"
    )

    remarks = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Bemerkung"
    )

    class Meta:

        ordering = [
            "name"
        ]

        verbose_name = "Betriebspunkt"
        verbose_name_plural = "Betriebspunkte"

    def __str__(self):

        return self.name