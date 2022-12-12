import sys
from collections import defaultdict

from travel.models import Airport, Connection


class VehicleInfo:
    FLIGHT = "flight"
    CAR = "car"
    TAXI = "taxi"
    INFO = {
        CAR: {"cost": 0.2, "passengers": 4, "fee": 3},
        TAXI: {"cost": 0.4, "passengers": 4, "fee": 0},
        FLIGHT: {"cost": 0.1, "passengers": 1, "fee": 0},
    }

    @classmethod
    def get_vehicles(cls):
        return cls.INFO.keys()

    @classmethod
    def get_vehicle_cost(cls, vehicle):
        return cls.INFO[vehicle]

    @classmethod
    def get_cost(cls, vehicle, distance, number_of_people=1):
        data = cls.get_vehicle_cost(vehicle)
        number_of_vehicles = -(number_of_people // -data["passengers"])
        return number_of_vehicles * ((distance * data["cost"]) + data["fee"])

    @classmethod
    def get_cheapest_quote(cls, distance, number_of_people=1):
        vehicles = cls.get_vehicles()
        return sorted(
            [
                (
                    VehicleInfo.get_cost(vehicle, distance, number_of_people),
                    vehicle,
                )
                for vehicle in vehicles
            ]
        )[0]

    @classmethod
    def get_all_connection_costs(cls):
        connection_data = defaultdict(dict)
        connections = Connection.objects.all()
        for connection in connections:
            from_id = connection.from_airport.code.lower()
            to_id = connection.to_airport.code.lower()
            connection_data[from_id][to_id] = cls.get_cost(
                cls.FLIGHT, connection.distance
            )
        return connection_data

    @classmethod
    def get_cheapest_air_quote(cls, from_id, to_id):
        connection_data = cls.get_all_connection_costs()
        unvisited_airports = [
            airport.lower()
            for airport in Airport.objects.all().values_list("code", flat=True)
        ]

        shortest_path = {}
        previous_nodes = {}
        for airport in unvisited_airports:
            shortest_path[airport] = sys.maxsize
        shortest_path[from_id] = 0

        while unvisited_airports:
            current_min_airport = None
            for airport in unvisited_airports:
                if current_min_airport is None:
                    current_min_airport = airport
                elif (
                    shortest_path[airport] < shortest_path[current_min_airport]
                ):
                    current_min_airport = airport

            for airport in connection_data[current_min_airport]:
                tentative_value = (
                    shortest_path[current_min_airport]
                    + connection_data[current_min_airport][airport]
                )
                if tentative_value < shortest_path[airport]:
                    shortest_path[airport] = tentative_value
                    previous_nodes[airport] = current_min_airport

            unvisited_airports.remove(current_min_airport)

        path = []
        source = to_id
        while True:
            path.append(source)
            if source == from_id:
                break
            source = previous_nodes[source]
        path.reverse()
        return shortest_path[to_id], path
