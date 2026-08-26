from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import UserProfile
from employees.models import Employee


class Command(BaseCommand):

    help = "Überträgt bestehende Employee-Daten in UserProfile"

    def handle(self, *args, **options):

        created = 0
        updated = 0
        skipped = 0

        employees = Employee.objects.select_related(
            "user",
            "category",
        ).all()

        for employee in employees:

            if not employee.user:

                self.stdout.write(
                    self.style.WARNING(
                        f"Übersprungen: "
                        f"{employee.first_name} "
                        f"{employee.last_name} "
                        f"(kein User verknüpft)"
                    )
                )

                skipped += 1
                continue

            user = employee.user

            profile, was_created = UserProfile.objects.update_or_create(

                user=user,

                defaults={
                    "entry_date": employee.entry_date,
                    "category": employee.category,
                    "etcs_authorized": employee.etcs_authorized,
                    "external_signal_authorized": employee.external_signal_authorized,
                    "role": employee.role,
                    "active": employee.active,
                },
            )

            if was_created:

                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Profil erstellt: "
                        f"{user.username}"
                    )
                )

            else:

                updated += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Profil aktualisiert: "
                        f"{user.username}"
                    )
                )

        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write(
            f"Erstellt: {created}"
        )
        self.stdout.write(
            f"Aktualisiert: {updated}"
        )
        self.stdout.write(
            f"Übersprungen: {skipped}"
        )
        self.stdout.write("=" * 50)