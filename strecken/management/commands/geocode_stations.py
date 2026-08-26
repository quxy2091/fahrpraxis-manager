from django.core.management.base import BaseCommand
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

from stations.models import Station


class Command(BaseCommand):

    help = "Ermittelt Koordinaten der Betriebspunkte über OpenStreetMap"

    def handle(self, *args, **kwargs):

        geolocator = Nominatim(
            user_agent="fahrpraxis_manager"
        )

        gefunden = 0
        nicht_gefunden = 0

        for station in Station.objects.order_by("name"):

            if station.x is not None and station.y is not None:
                continue

            suchbegriffe = [

                f"{station.name} Bahnhof Schweiz",

                f"{station.name} SBB",

                f"{station.name} Schweiz",

                station.name,

            ]

            location = None

            for begriff in suchbegriffe:

                try:

                    location = geolocator.geocode(
                        begriff,
                        timeout=15
                    )

                except (
                    GeocoderTimedOut,
                    GeocoderUnavailable,
                ):

                    continue

                if location:
                    break

            if location:

                station.x = location.longitude
                station.y = location.latitude

                station.save()

                gefunden += 1

                self.stdout.write(

                    self.style.SUCCESS(

                        f"{station.name:<35}"

                        f"{location.latitude:.6f}"

                        "  "

                        f"{location.longitude:.6f}"

                    )

                )

            else:

                nicht_gefunden += 1

                self.stdout.write(

                    self.style.WARNING(

                        f"Nicht gefunden: {station.name}"

                    )

                )

            time.sleep(1)

        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Gefunden: {gefunden}")
        self.stdout.write(f"Nicht gefunden: {nicht_gefunden}")