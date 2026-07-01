from stations.models import Station

with open(
    "betriebspunkte_liste.txt",
    encoding="utf-8"
) as f:

    for line in f:

        name = line.strip()

        if not name:
            continue

        if len(name) < 2:
            continue

        Station.objects.get_or_create(
            name=name
        )

print("Import abgeschlossen")