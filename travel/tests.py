import pytest

from common.helpers import VehicleInfo
from setup_db.load_data import load


@pytest.mark.parametrize(
    "distance, number_of_people, expected_cost, expected_vehicle",
    [
        (50, 6, 26, "car"),
        (1, 1, 0.1, "flight"),
        (0, 0, 0, "car"),
        (8, 4, 3.2, "flight"),
    ],
)
def test_cheapest_travel(
    distance, number_of_people, expected_cost, expected_vehicle
):
    cost, vehicle = VehicleInfo.get_cheapest_quote(distance, number_of_people)
    assert cost == expected_cost
    assert vehicle == expected_vehicle


@pytest.mark.parametrize(
    "distance, number_of_people, expected_cost, expected_vehicle",
    [
        (50, 6, 26, "car"),
        (1, 1, 0.1, "flight"),
        (0, 0, 0, "car"),
        (8, 4, 3.2, "flight"),
    ],
)
def test_cheapest_travel_api(
    distance, number_of_people, expected_cost, expected_vehicle, client
):
    response = client.get(f"/vehicle/{number_of_people}/{distance}")
    result = response.json()
    assert response.status_code == 200
    assert expected_cost == result["cost"]
    assert expected_vehicle == result["vehicle"]


def cheapest_air_quote():
    for from_id, to_id, expected_quote, expected_path in [
        ("fra", "fco", 25.0, ["fra", "zrh", "fco"]),
        ("fra", "vko", 107.0, ["fra", "muc", "vie", "vko"]),
        ("osl", "vko", 50.0, ["osl", "led", "svo", "vko"]),
    ]:
        quote, path = VehicleInfo.get_cheapest_air_quote(from_id, to_id)
        assert quote == expected_quote
        assert path == expected_path


def airports_api(client):
    response = client.get(f"/airports")
    result = response.json()
    assert response.status_code == 200
    assert "airport_names" in result
    assert len(result["airport_names"]) == 20


def cheapest_air_quote_api(client):
    for from_id, to_id, expected_quote, expected_path in [
        ("fra", "fco", 25.0, ["fra", "zrh", "fco"]),
        ("fra", "vko", 107.0, ["fra", "muc", "vie", "vko"]),
        ("osl", "vko", 50.0, ["osl", "led", "svo", "vko"]),
    ]:
        response = client.get(f"/airports/{from_id}/to/{to_id}")
        result = response.json()
        assert response.status_code == 200
        assert result["quote"] == expected_quote
        assert result["path"] == expected_path


def airport_data_api(client):
    for airport_id, expected_data in [
        (
            "fra",
            {
                "code": "FRA",
                "name": "Frankfurt Airport",
                "latitude": 50.033333,
                "longitude": 8.570556,
            },
        ),
        (
            "lgw",
            {
                "code": "LGW",
                "name": "Gatwick Airport",
                "latitude": 51.148056,
                "longitude": -0.190278,
            },
        ),
        (
            "dme",
            {
                "code": "DME",
                "name": "Moscow Domodedovo Airport",
                "latitude": 55.408611,
                "longitude": 37.906111,
            },
        ),
    ]:
        response = client.get(f"/airports/{airport_id}")
        assert response.status_code == 200
        assert response.json() == expected_data


@pytest.mark.django_db(transaction=True)
def test_with_db(client):
    load()
    cheapest_air_quote()
    airports_api(client)
    cheapest_air_quote_api(client)
    airport_data_api(client)
