import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from common.helpers import VehicleInfo
from common.http_status import status_types
from travel.models import Airport
from travel.serializers import AirportSerializer


class AirportView(viewsets.ViewSet):
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_description="Get the details of a given airport",
        responses={
            status_code: status_types[status_code]
            for status_code in [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ]
        },
    )
    def retrieve(self, _request, *_args, **kwargs):
        try:
            airport = Airport.objects.get(code__iexact=kwargs["pk"])
            return Response(
                AirportSerializer(airport).data, status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.exception("AirportView retrieve")
            logging.error("AirportView retrieve {}".format(error))
            return Response(
                {"message": "server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Fetch the list of airport names",
        responses={
            status_code: status_types[status_code]
            for status_code in [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ]
        },
    )
    def list(self, _request, *_args, **_kwargs):
        try:
            airport_names = Airport.objects.all().values_list(
                "name", flat=True
            )
            return Response(
                {"airport_names": airport_names}, status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.exception("CheapestVehicle list")
            logging.error("CheapestVehicle list {}".format(error))
            return Response(
                {"message": "server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AirportQuoteView(viewsets.ViewSet):
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_description="Get the quote to travel from a given airport to the destination airport",
        params=[
            openapi.Parameter(
                "from_id",
                openapi.IN_PATH,
                description="Id of the source airport",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "to_id",
                openapi.IN_PATH,
                description="Id of the destination airport",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            status_code: status_types[status_code]
            for status_code in [
                status.HTTP_200_OK,
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ]
        },
    )
    def list(self, _request, *_args, **kwargs):
        try:
            from_id = kwargs.get("from_id")
            to_id = kwargs.get("to_id")
            quote, path = VehicleInfo.get_cheapest_air_quote(
                from_id.lower(), to_id.lower()
            )
            return Response(
                {"quote": quote, "path": path}, status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.exception("AirportQuoteView list")
            logging.error("AirportQuoteView list {}".format(error))
            return Response(
                {"message": "server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
