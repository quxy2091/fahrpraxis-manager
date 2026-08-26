import fitz

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Liest alle Textobjekte aus der Streckenkarte"

    def handle(self, *args, **kwargs):

        pdf = fitz.open("Streckenkarte.pdf")

        page = pdf[0]

        blocks = page.get_text("dict")["blocks"]

        print()

        print("=" * 80)
        print("TEXTOBJEKTE")
        print("=" * 80)

        gefunden = 0

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

                x = round(line["bbox"][0], 1)
                y = round(line["bbox"][1], 1)

                print(
                    f"{x:7} {y:7}   {text}"
                )

                gefunden += 1

        print()
        print("=" * 80)
        print(f"{gefunden} Texte gefunden.")