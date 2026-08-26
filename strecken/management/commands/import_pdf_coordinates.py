import fitz

from django.core.management.base import BaseCommand

from stations.models import Station


class Command(BaseCommand):

    help = "Importiert Koordinaten aus der PDF"

    def handle(self, *args, **kwargs):

        pdf = fitz.open("Streckenkarte.pdf")

        page = pdf[0]

        words = page.get_text("words")

        stations = {}

        for s in Station.objects.all():

            stations[s.name.lower()] = s

        gefunden = 0

        for w in words:

            x0, y0, x1, y1, text, *_ = w

            text = text.strip()

            if len(text) < 2:
                continue

            station = stations.get(text.lower())

            if station:

                station.x = round((x0 + x1) / 2, 1)
                station.y = round((y0 + y1) / 2, 1)

                station.save()

                gefunden += 1

                print(
                    f"{station.name:<30}"
                    f"{station.x:>8}"
                    f"{station.y:>8}"
                )

        print()
        print("=" * 60)
        print(f"Gefunden: {gefunden}")