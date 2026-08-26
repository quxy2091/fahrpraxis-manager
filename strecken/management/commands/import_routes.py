from django.core.management.base import BaseCommand

from strecken.models import Route


ROUTES = [

(101,"Genève Aéroport - La Plaine - Genève - Genève-La-Praille"),
(102,"Annemasse - Genève"),
(111,"Genève-La-Praille - Lausanne"),
(121,"Lausanne - Fribourg/Freiburg - Bern"),
(141,"Bern - Burgdorf - Olten"),
(142,"Bern - NBS - Olten"),
(151,"Olten - Brugg AG"),
(161,"Brugg AG - Dietikon - Zürich HB"),
(171,"RBL - Wettingen - Zürich Oerlikon"),
(201,"Vallorbe - Lausanne"),
(202,"Vallorbe - Le Brassus"),
(203,"Orbe - Chavornay"),
(211,"Lausanne - Sion"),
(221,"Sion - Brig"),
(222,"Brig - Domo"),
(231,"Puidoux - Vevey"),
(232,"St-Gingolph - St-Maurice"),
(241,"Lausanne-Triage - Lausanne"),
(251,"Palézieux - Payerne"),
(252,"Payerne - Lyss - Büren"),
(254,"Broc-Chocolaterie - Romont"),
(255,"Fribourg - Murten - Ins - Neuchâtel"),
(261,"Yverdon-les-Bains - Fribourg"),
(271,"Pontarlier - Neuchâtel"),
(272,"Le Locle-Col-des-Roches - Neuchâtel"),
(273,"Travers - Buttes"),
(281,"La Chaux-de-Fonds - Biel/Bienne"),
(282,"Moutier - Tavannes - Biel"),
(291,"Delémont - Lengnau - Biel/Bienne"),
(292,"Delle - Delémont"),
(301,"Lausanne - Biel/Bienne"),
(311,"Biel/Bienne - Oensingen - Olten"),
(321,"Biel - Bern Weyermannshaus"),
(322,"Löchligut - Münsingen - Reichenbach"),
(331,"Bern - Langnau"),
(332,"Langnau - Luzern"),
(341,"Basel - Delémont"),
(351,"Reichenbach - Kandersteg - Brig"),
(361,"Spiez - Interlaken Ost"),
(362,"Spiez - Zweisimmen"),
(371,"Bern - Belp - Thun"),
(372,"Bern - Schwarzenburg"),
(381,"Bern - Neuchâtel"),
(391,"Reichenbach - LBS - Visp"),
(411,"Basel SBB - Gelterkinden - Olten"),
(421,"Sissach - Läufelfingen - Olten"),
(422,"Olten - Rothrist - Luzern"),
(431,"Luzern - Lenzburg"),
(436,"Zofingen - Lenzburg - Wettingen"),
(453,"Luzern - Horw"),
(461,"Zug - Luzern"),
(462,"Thalwil - Arth-Goldau"),
(481,"Solothurn - Moutier"),
(482,"Solothurn - Burgdorf"),
(483,"Burgdorf - Langnau"),
(484,"Burgdorf - Thun"),
(491,"Ramsei - Sumiswald"),
(493,"Langenthal - Wolhusen"),
(501,"Basel St. Johann - Pratteln"),
(502,"Basel Hafen - Basel RB"),
(511,"Basel SBB - Brugg AG"),
(521,"Brugg AG - Lenzburg - Rotkreuz"),
(531,"Rotkreuz - Göschenen"),
(532,"Luzern - Arth-Goldau"),
(533,"Altdorf - GBT - Bellinzona"),
(541,"Göschenen - Bellinzona"),
(542,"Bellinzona - Chiasso"),
(551,"Bellinzona - Locarno"),
(552,"Bellinzona - Luino"),
(601,"Stein-Säckingen - Koblenz"),
(602,"Koblenz - Winterthur"),
(611,"Schaffhausen - Bülach - Zürich Oerlikon"),
(612,"Niederweningen - Oberglatt"),
(631,"Zürich HB - Pfäffikon SZ"),
(632,"Zug - Zürich Altstetten"),
(635,"Zürich Wiedikon - Sihlbrugg"),
(636,"Zürich HB SZU - Uetliberg"),
(641,"Pfäffikon SZ - Sargans"),
(642,"Buchs SG - Chur"),
(651,"Zürich - Meilen - Rapperswil"),
(652,"Zürich Oerlikon - Uster - Rapperswil"),
(661,"Zürich - Stettbach - Hinwil"),
(701,"Zürich Altstetten - Zürich Oerlikon"),
(702,"Zürich Oerlikon - Winterthur"),
(711,"Winterthur - St. Gallen"),
(721,"St. Gallen - Buchs SG"),
(731,"Schaffhausen - Winterthur"),
(732,"Winterthur - Etzwilen"),
(741,"Winterthur - Romanshorn"),
(742,"Sulgen - Gossau SG"),
(751,"Rapperswil - Linthal"),
(752,"Pfäffikon SZ - Wattwil"),
(753,"Nesslau - Wil"),
(754,"Winterthur - Wald - Rapperswil"),
(761,"Konstanz - Wil"),
(771,"Schaffhausen - Kreuzlingen"),
(772,"Konstanz - Rorschach"),
(781,"Pfäffikon SZ - Arth-Goldau"),
(782,"Wädenswil - Einsiedeln"),
(791,"Wattwil - St. Gallen - Romanshorn"),

]


class Command(BaseCommand):

    help = "Importiert alle offiziellen Strecken"

    def handle(self,*args,**kwargs):

        Route.objects.all().delete()

        for number,name in ROUTES:

            Route.objects.create(
                number=number,
                name=name,
            )

            self.stdout.write(
                f"✓ {number} {name}"
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(ROUTES)} Strecken importiert."
            )
        )