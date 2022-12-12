from django.urls import include, path
from rest_framework.routers import DefaultRouter

from travel.views.airports import AirportQuoteView, AirportView
from travel.views.cheapest import CheapestVehicle

router = DefaultRouter(trailing_slash=False)

router.register(
    r"vehicle/(?P<number_of_people>\d+)/(?P<distance>\d+)",
    CheapestVehicle,
    "cheapestVehicle",
)

router.register(
    r"airports/(?P<from_id>\w+)/to/(?P<to_id>\w+)",
    AirportQuoteView,
    "airportQuoteView",
)
router.register("airports", AirportView, "airportView")

urlpatterns = [path("", include(router.urls))]
