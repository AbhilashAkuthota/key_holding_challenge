import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from common.helpers import VehicleInfo
from common.http_status import status_types


class CheapestVehicle(viewsets.ViewSet):
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_description="Get the cheapest vehicle to use for given number of people and the distance in miles",
        params=[
            openapi.Parameter(
                "number_of_people",
                openapi.IN_PATH,
                description="Number of people to travel",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "miles",
                openapi.IN_PATH,
                description="Total distance in miles to travel",
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
            number_of_people = int(kwargs.get("number_of_people"))
            distance = int(kwargs.get("distance"))
            cost, vehicle = VehicleInfo.get_cheapest_quote(
                distance, number_of_people
            )

            return Response(
                {"vehicle": vehicle, "cost": cost}, status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.exception("CheapestVehicle list")
            logging.error("CheapestVehicle list {}".format(error))
            return Response(
                {"message": "server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
