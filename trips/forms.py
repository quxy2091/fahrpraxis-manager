from django import forms

from .models import Trip


class TripForm(forms.ModelForm):

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        )
    )

    class Meta:

        model = Trip

        fields = [
            "date",
            "train_number",
            "service_type",
            "vehicle",
            "etcs",
            "hours",
            "notes",
        ]