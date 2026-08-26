from datetime import date
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from accounts.models import UserProfile

from trips.models import Trip

from .forms import UserProfileForm


@login_required
def employee_list(request):

    current_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not current_profile:
        return redirect("/")

    if current_profile.role != "admin":
        return redirect("/")

    profiles = UserProfile.objects.all().select_related(
        "user",
        "category",
    ).order_by(
        "user__last_name",
        "user__first_name",
    )

    return render(
        request,
        "employees/employee_list.html",
        {
            "employees": profiles
        }
    )


@login_required
def employee_create(request):

    current_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not current_profile:
        return redirect("/")

    if current_profile.role != "admin":
        return redirect("/")

    if request.method == "POST":

        form = UserProfileForm(
            request.POST
        )

        if form.is_valid():

            profile = form.save()

            messages.success(
                request,
                "Benutzer erfolgreich erstellt."
            )

            return redirect(
                "employee_dashboard",
                employee_id=profile.id
            )

    else:

        form = UserProfileForm()

    return render(
        request,
        "employees/employee_create.html",
        {
            "form": form,
        }
    )


@login_required
def employee_dashboard(
    request,
    employee_id,
    year=None
):

    current_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not current_profile:
        return redirect("/")

    if current_profile.role != "admin":
        return redirect("/")

    profile = get_object_or_404(
        UserProfile.objects.select_related(
            "user",
            "category",
        ),
        pk=employee_id
    )

    today = date.today()

    base_year = today.year

    if year is None:
        current_year = base_year
    else:
        current_year = year

    # ==============================================
    # VERFÜGBARE JAHRE
    # ==============================================

    available_years = set()

    # Aktuelles Jahr immer anzeigen
    available_years.add(
        base_year
    )

    # Vergangene Jahre nur dann anzeigen,
    # wenn für diesen Mitarbeiter Fahrten vorhanden sind
    trip_years = (
        Trip.objects
        .filter(
            user_profile=profile,
            date__lt=date(base_year, 1, 1)
        )
        .dates(
            "date",
            "year",
            order="DESC"
        )
    )

    for year_date in trip_years:

        available_years.add(
            year_date.year
        )

    # Ab 1. Dezember bereits das kommende
    # Jahr anzeigen
    if today.month >= 12:

        available_years.add(
            base_year + 1
        )

    available_years = sorted(
        available_years,
        reverse=True
    )

    # ==============================================
    # FAHRTEN DES GEWÄHLTEN JAHRES
    # ==============================================

    trips = Trip.objects.filter(
        user_profile=profile,
        date__year=current_year
    ).order_by(
        "-date"
    )

    total_hours = sum(
        trip.hours for trip in trips
    )

    if profile.category:

        target_hours = (
            profile.category.yearly_target_hours
        )

    else:

        target_hours = 0

    percent = 0

    if target_hours > 0:

        percent = round(
            (total_hours / target_hours) * 100,
            1
        )

    remaining = max(
        target_hours - total_hours,
        0
    )

    return render(
        request,
        "employees/employee_dashboard.html",
        {
            "employee": profile,
            "profile": profile,

            "base_year": base_year,
            "current_year": current_year,
            "available_years": available_years,

            "trips": trips,

            "total_hours": total_hours,
            "target_hours": target_hours,
            "percent": percent,
            "remaining": remaining,
        }
    )


@login_required
def employee_year_pdf(
    request,
    employee_id,
    year
):

    current_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not current_profile:
        return redirect("/")

    if current_profile.role != "admin":
        return redirect("/")

    profile = get_object_or_404(
        UserProfile.objects.select_related(
            "user",
            "category",
        ),
        pk=employee_id
    )

    # ==============================================
    # FAHRTEN DES GEWÄHLTEN JAHRES
    # ==============================================

    trips = Trip.objects.filter(
        user_profile=profile,
        date__year=year
    ).order_by(
        "date"
    )

    total_hours = sum(
        trip.hours for trip in trips
    )

    if profile.category:

        target_hours = (
            profile.category.yearly_target_hours
        )

    else:

        target_hours = 0

    remaining = max(
        target_hours - total_hours,
        0
    )

    percent = 0

    if target_hours > 0:

        percent = round(
            (total_hours / target_hours) * 100,
            1
        )

    # ==============================================
    # PDF
    # ==============================================

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,

        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,

        title=(
            f"Fahrpraxis {year} - "
            f"{profile.user.get_full_name()}"
        ),

        author="Semita Fahrpraxis Manager",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "SemitaTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#244C82"),
        spaceAfter=6,
    )

    heading_style = ParagraphStyle(
        "SemitaHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#244C82"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "SemitaNormal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    small_style = ParagraphStyle(
        "SemitaSmall",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
    )

    story = []

    # ==============================================
    # LOGO
    # ==============================================

    logo_path = (
        settings.BASE_DIR
        / "dashboard"
        / "static"
        / "images"
        / "semita.png"
    )

    if logo_path.exists():

        logo = Image(
            str(logo_path),
            width=45 * mm,
            height=15 * mm,
            kind="proportional",
        )

        logo.hAlign = "LEFT"

    else:

        logo = Paragraph(
            "<b>SEMITA</b>",
            title_style
        )

    # ==============================================
    # PDF HEADER
    # ==============================================

    header_right = Paragraph(
        f"<b>Fahrpraxis-Jahresauswertung</b><br/>"
        f"Jahr {year}",
        ParagraphStyle(
            "HeaderRight",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=2,
        )
    )

    header_table = Table(
        [
            [
                logo,
                header_right,
            ]
        ],
        colWidths=[
            90 * mm,
            90 * mm,
        ]
    )

    header_table.setStyle(
        TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "ALIGN",
                (1, 0),
                (1, 0),
                "RIGHT",
            ),
            (
                "LINEBELOW",
                (0, 0),
                (-1, 0),
                1,
                colors.HexColor("#244C82"),
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                10,
            ),
        ])
    )

    story.append(
        header_table
    )

    story.append(
        Spacer(
            1,
            7 * mm
        )
    )

    # ==============================================
    # TITEL
    # ==============================================

    story.append(
        Paragraph(
            f"Fahrpraxis {year}",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Jahresauswertung",
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            4 * mm
        )
    )

    # ==============================================
    # MITARBEITER
    # ==============================================

    story.append(
        Paragraph(
            "Mitarbeiter",
            heading_style
        )
    )

    full_name = (
        profile.user.get_full_name()
        or profile.user.email
    )

    category = (
        str(profile.category)
        if profile.category
        else "Keine Kategorie"
    )

    etcs = []

    if profile.etcs_level1:

        etcs.append(
            "ETCS Level 1"
        )

    if profile.etcs_level2:

        etcs.append(
            "ETCS Level 2"
        )

    etcs_text = (
        ", ".join(etcs)
        if etcs
        else "Keine ETCS-Berechtigung"
    )

    employee_data = [

        [
            Paragraph(
                "<b>Name</b>",
                normal_style
            ),
            Paragraph(
                full_name,
                normal_style
            ),
        ],

        [
            Paragraph(
                "<b>E-Mail</b>",
                normal_style
            ),
            Paragraph(
                profile.user.email or "-",
                normal_style
            ),
        ],

        [
            Paragraph(
                "<b>Kategorie</b>",
                normal_style
            ),
            Paragraph(
                category,
                normal_style
            ),
        ],

        [
            Paragraph(
                "<b>ETCS</b>",
                normal_style
            ),
            Paragraph(
                etcs_text,
                normal_style
            ),
        ],

    ]

    employee_table = Table(
        employee_data,
        colWidths=[
            35 * mm,
            145 * mm,
        ]
    )

    employee_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#f3f6fa"),
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#cccccc"),
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.25,
                colors.HexColor("#dddddd"),
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])
    )

    story.append(
        employee_table
    )

    # ==============================================
    # ZUSAMMENFASSUNG
    # ==============================================

    story.append(
        Paragraph(
            f"Fahrpraxis {year}",
            heading_style
        )
    )

    summary_data = [

        [
            Paragraph(
                "<b>Sollstunden</b>",
                normal_style
            ),
            Paragraph(
                f"{target_hours} h",
                normal_style
            ),
            Paragraph(
                "<b>Iststunden</b>",
                normal_style
            ),
            Paragraph(
                f"{total_hours} h",
                normal_style
            ),
        ],

        [
            Paragraph(
                "<b>Reststunden</b>",
                normal_style
            ),
            Paragraph(
                f"{remaining} h",
                normal_style
            ),
            Paragraph(
                "<b>Fortschritt</b>",
                normal_style
            ),
            Paragraph(
                f"{percent} %",
                normal_style
            ),
        ],

    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            35 * mm,
            55 * mm,
            35 * mm,
            55 * mm,
        ]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#f5f7fb"),
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#cccccc"),
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.25,
                colors.HexColor("#dddddd"),
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),
        ])
    )

    story.append(
        summary_table
    )

    # ==============================================
    # FAHRTEN
    # ==============================================

    story.append(
        Paragraph(
            f"Fahrten {year}",
            heading_style
        )
    )

    trip_data = [

        [
            Paragraph(
                "<b>Datum</b>",
                small_style
            ),
            Paragraph(
                "<b>Verkehr</b>",
                small_style
            ),
            Paragraph(
                "<b>Zug</b>",
                small_style
            ),
            Paragraph(
                "<b>Von</b>",
                small_style
            ),
            Paragraph(
                "<b>Nach</b>",
                small_style
            ),
            Paragraph(
                "<b>Fahrzeug</b>",
                small_style
            ),
            Paragraph(
                "<b>Std.</b>",
                small_style
            ),
        ]

    ]

    for trip in trips:

        if trip.traffic_type == "zug":

            traffic = "Zug"

        elif trip.traffic_type == "rangieren":

            traffic = "Rangierbewegung"

        else:

            traffic = str(
                trip.traffic_type
            )

        trip_data.append(

            [

                trip.date.strftime(
                    "%d.%m.%Y"
                ),

                traffic,

                trip.train_number or "-",

                trip.from_station or "-",

                trip.to_station or "-",

                str(trip.vehicle)
                if trip.vehicle
                else "-",

                str(trip.hours),

            ]

        )

    if len(trip_data) == 1:

        trip_data.append(

            [
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
                "Keine Fahrten",
            ]

        )

    trip_table = Table(
        trip_data,
        repeatRows=1,
        colWidths=[
            22 * mm,
            28 * mm,
            20 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
            15 * mm,
        ]
    )

    trip_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#244C82"),
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.25,
                colors.HexColor("#cccccc"),
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f7f9fb"),
                ],
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5,
            ),

        ])
    )

    story.append(
        trip_table
    )

    # ==============================================
    # PDF ERZEUGEN
    # ==============================================

    document.build(
        story
    )

    buffer.seek(0)

    filename = (
        f"Fahrpraxis_"
        f"{profile.user.last_name}_"
        f"{year}.pdf"
    )

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )


@login_required
def employee_edit(
    request,
    employee_id
):

    current_profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if not current_profile:
        return redirect("/")

    if current_profile.role != "admin":
        return redirect("/")

    profile = get_object_or_404(
        UserProfile.objects.select_related(
            "user",
            "category",
        ),
        pk=employee_id
    )

    if request.method == "POST":

        form = UserProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Benutzerdaten erfolgreich gespeichert."
            )

            return redirect(
                "employee_dashboard",
                employee_id=profile.id
            )

    else:

        form = UserProfileForm(
            instance=profile
        )

    return render(
        request,
        "employees/employee_edit.html",
        {
            "form": form,
            "employee": profile,
            "profile": profile,
        }
    )