from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import UserProfile

from .forms import TripForm
from .models import Trip


@login_required
def trip_list(request):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        return redirect("/")

    trips = Trip.objects.filter(
        user_profile=profile
    ).order_by(
        "-date",
        "-created_at"
    )

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips,
            "profile": profile,
        }
    )


@login_required
def create_trip(request):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        return redirect("/")

    if request.method == "POST":

        form = TripForm(request.POST)

        if form.is_valid():

            trip = form.save(
                commit=False
            )

            trip.user_profile = profile

            trip.save()

            messages.success(
                request,
                "Fahrt erfolgreich gespeichert."
            )

            return redirect(
                "/mein-cockpit/"
            )

    else:

        form = TripForm()

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "title": "Neue Fahrt erfassen",
            "button_text": "Fahrt speichern",
        }
    )


@login_required
def edit_trip(
    request,
    trip_id
):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        return redirect("/")

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        user_profile=profile
    )

    if request.method == "POST":

        form = TripForm(
            request.POST,
            instance=trip
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fahrt erfolgreich geändert."
            )

            return redirect(
                "/mein-cockpit/"
            )

    else:

        form = TripForm(
            instance=trip
        )

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "trip": trip,
            "title": "Fahrt bearbeiten",
            "button_text": "Änderungen speichern",
        }
    )


@login_required
def delete_trip(
    request,
    trip_id
):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        return redirect("/")

    trip = get_object_or_404(
        Trip,
        pk=trip_id,
        user_profile=profile
    )

    if request.method == "POST":

        trip.delete()

        messages.success(
            request,
            "Fahrt erfolgreich gelöscht."
        )

        return redirect(
            "/mein-cockpit/"
        )

    return render(
        request,
        "trips/delete_trip.html",
        {
            "trip": trip
        }
    )


@login_required
def trip_pdf(request):

    profile = UserProfile.objects.filter(
        user=request.user
    ).first()

    if profile is None:
        return redirect("/")

    trips = Trip.objects.filter(
        user_profile=profile
    ).order_by(
        "date",
        "created_at"
    )

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.platypus import Spacer
    from reportlab.platypus import Table
    from reportlab.platypus import TableStyle

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        'inline; filename="fahrten.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "PDFNormal",
        parent=styles["Normal"],
        fontSize=9,
    )

    small_style = ParagraphStyle(
        "PDFSmall",
        parent=styles["Normal"],
        fontSize=7,
    )

    elements = []

    full_name = (
        request.user.get_full_name()
        or request.user.username
    )

    elements.append(
        Paragraph(
            "Semita Fahrpraxis Manager",
            title_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Fahrtenübersicht</b><br/>"
            f"{full_name}<br/>"
            f"{request.user.email}",
            normal_style
        )
    )

    elements.append(
        Spacer(
            1,
            8 * mm
        )
    )

    table_data = [
        [
            "Datum",
            "Zug",
            "Von",
            "Nach",
            "Verkehr",
            "Fahrzeug",
            "Std.",
        ]
    ]

    total_hours = 0

    for trip in trips:

        total_hours += trip.hours

        table_data.append(
            [
                trip.date.strftime(
                    "%d.%m.%Y"
                ),
                trip.train_number
                or "Rangieren",
                str(
                    trip.from_station
                ),
                str(
                    trip.to_station
                    or ""
                ),
                trip.get_traffic_type_display(),
                str(
                    trip.vehicle
                    or ""
                ),
                f"{trip.hours:.2f}",
            ]
        )

    table_data.append(
        [
            "",
            "",
            "",
            "",
            "",
            "Total",
            f"{total_hours:.2f}",
        ]
    )

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            24 * mm,
            22 * mm,
            30 * mm,
            30 * mm,
            30 * mm,
            32 * mm,
            16 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#0A2740"
                    ),
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
                    (-1, 0),
                    8,
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    7,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (-1, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "FONTNAME",
                    (-2, -1),
                    (-1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "BACKGROUND",
                    (0, -1),
                    (-1, -1),
                    colors.HexColor(
                        "#eef2f7"
                    ),
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
            ]
        )
    )

    elements.append(table)

    elements.append(
        Spacer(
            1,
            8 * mm
        )
    )

    elements.append(
        Paragraph(
            f"<b>Total Fahrpraxis: "
            f"{total_hours:.2f} Stunden</b>",
            normal_style
        )
    )

    document.build(
        elements
    )

    return response