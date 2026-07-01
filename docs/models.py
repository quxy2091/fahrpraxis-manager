from django.db import models


class Document(models.Model):

    CATEGORY_CHOICES = [
        ("planung", "Planung"),
        ("mitteilung", "Mitteilung"),
        ("weisung", "Weisung"),
        ("formular", "Formular"),
    ]

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.title