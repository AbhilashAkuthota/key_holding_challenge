import json

from setup_db.local_data import data
from travel.models import Airport, Connection


def load():
    all_connections = []
    airports = {}

    print("Saving airports")
    for entry in data:
        code, name, latitude, longitude, connections = entry

        airport = Airport(
            code=code, name=name, latitude=latitude, longitude=longitude
        )
        airport.save()
        airports[code] = airport
        all_connections.append((code, json.loads(connections)))

    print("Saving airport connections")
    for connections in all_connections:
        code, connections = connections
        for connection in connections:
            from_airport = airports[code]
            to_airport = airports[connection["id"]]
            connection = Connection(
                from_airport=from_airport,
                to_airport=to_airport,
                distance=connection["miles"],
            )
            connection.save()
