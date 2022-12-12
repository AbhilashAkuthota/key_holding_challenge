from rest_framework import serializers

from travel.models import Airport, Connection


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        exclude = ("id", "created_at", "updated_at")


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        exclude = ("id", "created_at", "updated_at")
