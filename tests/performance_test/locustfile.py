from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("")

    @task
    def show_summary_page(self):
        email = "john@simplylift.co"
        self.client.post("showSummary", data={"email": email})

    @task
    def show_clubs_page(self):
        self.client.get("showClubs")

    @task
    def purchase_places_page(self):
        club = "Simply Lift"
        competition = "Spring Festival"
        points = 1
        self.client.post("purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})

    @task
    def book_competition_club_page(self):
        self.client.get("book/Spring%20Festival/Simply%20Lift")

    @task
    def logout_page(self):
        self.client.get("logout")