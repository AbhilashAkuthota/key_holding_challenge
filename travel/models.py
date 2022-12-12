from django.db import models

from common.models import BaseModel


class Airport(BaseModel):
    code = models.CharField(
        max_length=128, unique=True, blank=False, null=False
    )
    name = models.CharField(max_length=128, blank=False, null=False)

    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} - {self.code}"


class Connection(BaseModel):
    from_airport = models.ForeignKey(
        Airport,
        related_name="from_airport",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    to_airport = models.ForeignKey(
        Airport,
        related_name="to_airport",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.from_airport} - {self.to_airport}"
