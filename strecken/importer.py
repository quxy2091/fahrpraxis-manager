import re

from strecken.models import Route


def import_routes(lines):

    created = 0
    updated = 0

    pattern = re.compile(
        r"^(\d{3,4})\s+(.+)$"
    )

    for line in lines:

        line = line.strip()

        match = pattern.match(line)

        if not match:
            continue

        number = int(match.group(1))

        name = match.group(2).strip()

        route, was_created = Route.objects.update_or_create(

            number=number,

            defaults={

                "name": name,
                "active": True,

            }

        )

        if was_created:

            created += 1

        else:

            updated += 1

    return created, updated