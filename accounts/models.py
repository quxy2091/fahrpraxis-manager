from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("employee", "Mitarbeiter"),
        ("admin", "Admin"),
    ]

    ETCS_CHOICES = [
        ("level1", "ETCS Level 1"),
        ("level2", "ETCS Level 2"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    entry_date = models.DateField(
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        "employees.Category",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profiles",
    )

    etcs_level1 = models.BooleanField(
        default=False,
    )

    etcs_level2 = models.BooleanField(
        default=False,
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="employee",
    )

    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return (
            self.user.get_full_name()
            or self.user.username
        )