from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from trips.models import Trip


class Command(BaseCommand):

    help = "Überträgt bestehende Fahrten von Employee auf UserProfile"

    def handle(self, *args, **options):

        updated = 0
        skipped = 0

        trips = Trip.objects.select_related(
            "employee",
            "employee__user",
        ).all()

        for trip in trips:

            if trip.user_profile_id:
                skipped += 1
                continue

            if not trip.employee_id:
                self.stdout.write(
                    self.style.WARNING(
                        f"Übersprungen: Fahrt {trip.id} "
                        f"hat keinen Employee."
                    )
                )
                skipped += 1
                continue

            employee = trip.employee

            if not employee.user_id:
                self.stdout.write(
                    self.style.WARNING(
                        f"Übersprungen: Fahrt {trip.id} "
                        f"für {employee} hat keinen User."
                    )
                )
                skipped += 1
                continue

            try:
                profile = UserProfile.objects.get(
                    user=employee.user
                )

            except UserProfile.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"Übersprungen: Fahrt {trip.id} "
                        f"für {employee}: kein UserProfile."
                    )
                )

                skipped += 1
                continue

            trip.user_profile = profile
            trip.save(
                update_fields=[
                    "user_profile",
                    "updated_at",
                ]
            )

            updated += 1

        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write(
            f"Fahrten übertragen: {updated}"
        )
        self.stdout.write(
            f"Übersprungen: {skipped}"
        )
        self.stdout.write("=" * 50)