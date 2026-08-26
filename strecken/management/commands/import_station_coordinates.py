import fitz

from django.core.management.base import BaseCommand

from rapidfuzz import process

from stations.models import Station


class Command(BaseCommand):

    help = "Importiert Stationskoordinaten direkt aus der PDF"

    def handle(self, *args, **kwargs):

        pdf = fitz.open("Streckenkarte.pdf")

        page = pdf[0]

        blocks = page.get_text("dict")["blocks"]

        stations = list(
            Station.objects.values_list(
                "name",
                flat=True
            )
        )

        gefunden = 0

        übersprungen = 0

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                text = ""

                for span in line["spans"]:

                    text += span["text"]

                text = text.strip()

                if len(text) < 2:
                    continue

                match = process.extractOne(

                    text,

                    stations,

                    score_cutoff=90

                )

                if match is None:

                    übersprungen += 1

                    continue

                station = Station.objects.get(
                    name=match[0]
                )

                x = line["bbox"][0]
                y = line["bbox"][1]

                station.x = round(x,1)
                station.y = round(y,1)

                station.save()

                gefunden += 1

                self.stdout.write(

                    f"{station.name:<35}"

                    f"{round(x):>5}"

                    f"{round(y):>5}"

                )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"{gefunden} Stationen gespeichert."
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"{übersprungen} Texte ignoriert."
            )
        )