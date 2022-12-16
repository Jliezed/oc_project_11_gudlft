import pytest

from oc_project_11_gudlft.server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


clubs_data = [{'name': 'Test Club', 'email': 'test@example.com', 'points': '13'},
              {'name': 'Test Club 2', 'email': 'test2@example.com', 'points': '13'}]

competitions_data = [{
    "name": "Competition Test",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "12",
    "Test Club 2": "12",
}]
