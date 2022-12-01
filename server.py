import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        error_message = "You don't have an account"
        return render_template('index.html', error_message=error_message)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][
        0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    new_competition_seats = int(competition['numberOfPlaces']) - placesRequired

    new_club_points = int(club['points']) - placesRequired
    try:
        current_club_seats_competition = int(competition[club["name"]])
    except KeyError:
        current_club_seats_competition = 0

    error_messages = []
    if new_club_points < 0:
        error_message = "You don't have enough points to book the seats requested"
        error_messages.append(error_message)
    if placesRequired > 12:
        error_message = "You can only book 12 seats maximum"
        error_messages.append(error_message)
    if current_club_seats_competition >= 12:
        error_message = "You already booked 12 seats for this competition"
        error_messages.append(error_message)
    else:
        with open('competitions.json', "w") as file:
            for comp in competitions:
                if comp["name"] == competition["name"]:
                    comp["numberOfPlaces"] = str(new_competition_seats)
                    # Save club seats for the competition
                    comp[club["name"]] = str(placesRequired +
                                             current_club_seats_competition)
            data = {
                "competitions": competitions,
            }
            json.dump(data, file)

        flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions,
                           error_messages=error_messages)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
