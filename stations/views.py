from dal import autocomplete

from .models import Station


class StationAutocomplete(
    autocomplete.Select2QuerySetView
):

    def get_queryset(self):

        if not self.request.user.is_authenticated:

            return Station.objects.none()

        qs = Station.objects.all()

        if self.q:

            qs = qs.filter(
                name__icontains=self.q
            )

        return qs.order_by(
            "name"
        )