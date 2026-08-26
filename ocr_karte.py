import cv2
import easyocr

from rapidfuzz import process

from stations.models import Station

reader = easyocr.Reader(
    ["de", "fr", "it", "en"],
    gpu=False
)

image = cv2.imread("karte.png")

result = reader.readtext(image)

stations = list(
    Station.objects.values_list(
        "name",
        flat=True
    )
)

print()

for r in result:

    box = r[0]

    text = r[1]

    score = r[2]

    if score < 0.35:
        continue

    match = process.extractOne(
        text,
        stations,
        score_cutoff=70
    )

    if match is None:
        continue

    name = match[0]

    x = int(
        sum(
            p[0] for p in box
        ) / 4
    )

    y = int(
        sum(
            p[1] for p in box
        ) / 4
    )

    station = Station.objects.get(
        name=name
    )

    station.x = x
    station.y = y
    station.save()

    print(
        f"{name:30}  {x:4} {y:4}"
    )

print("\nFertig.")