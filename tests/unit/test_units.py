from pathlib import Path

import os

from oc_project_11_gudlft.tests.conftest import clubs_data, competitions_data
from oc_project_11_gudlft.server import loadClubs, loadCompetitions
from oc_project_11_gudlft import server

tests_unit_dir = Path(__file__).parent

def test_load_clubs_file_not_empty():
    """ Test that clubs database is not empty """
    data_clubs = loadClubs()
    assert data_clubs != ""


def test_load_competitions_file_not_empty():
    """ Test that competitions database is not empty """
    data_competitions = loadCompetitions()
    assert data_competitions != ""


def setUp():
    with open(tests_unit_dir / 'clubs.json') as database:
        clubs = []
    with open(tests_unit_dir / 'competitions.json') as database:
        competitions = []
        return clubs, competitions


class TestClass:
    def test_index_page(self, client):
        """ Test response to index page and returned data """
        response = client.get('/')
        data = response.data.decode()
        assert response.status_code == 200
        assert "Welcome" in data

    def test_index_unkwown_email(self, client):
        """ Test response for unknown email """
        email = "unknown@email.com"
        response = client.post("/showSummary", data={"email": email})
        data = response.data.decode()

        assert response.status_code == 200
        assert "You don&#39;t have an account" in data

    def test_show_summary_page(self, client, mocker):
        """ Test response for email included into the database """
        mocker.patch.object(server, "clubs", clubs_data)
        new_club_email = "test@example.com"

        response = client.post("/showSummary", data={"email": new_club_email})
        data = response.data.decode()
        assert response.status_code == 200
        assert "<h2>Welcome, test@example.com </h2>" in data

    def test_show_clubs_page(self, client):
        response = client.get("/showClubs")
        data = response.data.decode()
        assert response.status_code == 200
        assert "<h3>Clubs:</h3>" in data

    def test_purchase_places_page(self, client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club"
        competition = "Competition Test"
        points = 1

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()

        assert response.status_code == 200
        assert "<li>Great-booking complete!</li>" in data

    def test_purchase_places_not_enough_points(self, client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club"
        competition = "Competition Test"
        points = 100

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()
        assert response.status_code == 200
        assert "You don&#39;t have enough points to book the seats requested</br>" in data

    def test_purchase_places_12_seats_limitation(self, client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club"
        competition = "Competition Test"
        points = 13

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()
        assert response.status_code == 200
        assert "You can only book 12 seats maximum</br>" in data

    def test_purchase_places_already_booked_12_seats(self, client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club 2"
        competition = "Competition Test"
        points = 12

        first_response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = first_response.data.decode()
        assert first_response.status_code == 200
        assert "You already booked 12 seats for this competition</br>" in data

    def test_book_competition_club_page(self, client):
        response = client.get('/book/Spring%20Festival/Simply%20Lift')
        data = response.data.decode()
        assert response.status_code == 200
        assert "<h2>Spring Festival</h2>" in data

    def test_logout_page(self, client):
        response = client.get('/logout')
        data = response.data.decode()
        assert response.status_code == 302
