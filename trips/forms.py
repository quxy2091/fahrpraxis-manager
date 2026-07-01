from datetime import date
import re

from django import forms
from django.core.exceptions import ValidationError

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
            "traffic_type",
            "shunting_type",
            "train_number",
            "from_station",
            "to_station",
            "vehicle",
            "hours",
            "notes",
        ]

        widgets = {

            "traffic_type": forms.Select(
                attrs={
                    "id": "id_traffic_type"
                }
            ),

            "shunting_type": forms.Select(
                attrs={
                    "id": "id_shunting_type"
                }
            ),

            "train_number": forms.TextInput(
                attrs={
                    "maxlength": "6",
                    "placeholder": "optional bei Rangierbewegung",
                    "autocomplete": "off",
                }
            ),

            "hours": forms.NumberInput(
                attrs={
                    "step": "0.25",
                    "min": "0.25",
                    "max": "24",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),
        }

    def clean_date(self):

        fahrdatum = self.cleaned_data["date"]

        if fahrdatum > date.today():

            raise ValidationError(
                "Das Fahrdatum darf nicht in der Zukunft liegen."
            )

        return fahrdatum

    def clean_train_number(self):

        value = self.cleaned_data.get(
            "train_number",
            ""
        )

        value = value.strip().upper()

        if value == "":

            return value

        if not re.fullmatch(
            r"\d{1,5}[A-Z]?",
            value
        ):

            raise ValidationError(
                "Erlaubt sind 1 bis 5 Ziffern und optional ein Buchstabe am Ende."
            )

        return value

    def clean_hours(self):

        hours = self.cleaned_data["hours"]

        if hours <= 0:

            raise ValidationError(
                "Die Fahrzeit muss grösser als 0 sein."
            )

        if hours > 24:

            raise ValidationError(
                "Eine einzelne Fahrt darf maximal 24 Stunden dauern."
            )

        return hours

    def clean(self):

        cleaned = super().clean()

        traffic = cleaned.get("traffic_type")
        shunting = cleaned.get("shunting_type")

        train_number = cleaned.get("train_number")

        from_station = cleaned.get("from_station")
        to_station = cleaned.get("to_station")

        if traffic == "zug":

            if not train_number:

                self.add_error(
                    "train_number",
                    "Bei einer Zugfahrt ist die Zugnummer obligatorisch."
                )

            if not to_station:

                self.add_error(
                    "to_station",
                    "Bei einer Zugfahrt muss ein Zielbetriebspunkt angegeben werden."
                )

        elif traffic == "rangieren":

            if not shunting:

                self.add_error(
                    "shunting_type",
                    "Bitte Direkt oder Indirekt auswählen."
                )

            if shunting == "indirekt":

                cleaned["vehicle"] = None

        if from_station and to_station:

            if from_station == to_station:

                self.add_error(
                    "to_station",
                    "Start- und Zielbetriebspunkt dürfen nicht identisch sein."
                )

        return cleaned