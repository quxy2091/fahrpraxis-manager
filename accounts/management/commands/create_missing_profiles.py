from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import UserProfile


class Command(BaseCommand):

    help = "Erstellt fehlende UserProfile für bestehende Django-Benutzer"

    def handle(self, *args, **options):

        created = 0
        existing = 0

        for user in User.objects.all().order_by("username"):

            profile, was_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "role": "employee",
                    "active": user.is_active,
                },
            )

            if was_created:

                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Profil erstellt: {user.username}"
                    )
                )

            else:

                existing += 1

                self.stdout.write(
                    f"Profil vorhanden: {user.username}"
                )

        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write(
            f"Neu erstellt: {created}"
        )
        self.stdout.write(
            f"Bereits vorhanden: {existing}"
        )
        self.stdout.write("=" * 50)