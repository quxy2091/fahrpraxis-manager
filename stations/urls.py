from django.urls import path

from .views import StationAutocomplete


urlpatterns = [

    path(
        "autocomplete/",
        StationAutocomplete.as_view(),
        name="station-autocomplete"
    ),

]