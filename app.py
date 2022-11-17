import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
# import creds  # create a creds.py file with a MOVIE_DB_API_KEY = 'xxxxxx'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox742ssdfgKR6b'
Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "garmin.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    address = db.Column(db.String(250))
    city = db.Column(db.String(100))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<course {self.name}>'

class users(db.Model):
    index_label = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(250))
    course = db.Column(db.String(250))
    city = db.Column(db.String(100))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    year = db.Column(db.Integer)
    best_match_score = db.Column(db.Float)
    good_match = db.Column(db.Boolean)
    garmin_ID = db.Column(db.String(100))
    g_course = db.Column(db.String(250))
    g_city = db.Column(db.String(100))
    g_state = db.Column(db.String(40))
    g_country = db.Column(db.String(40))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


@app.route("/")
def home():

    matches = users.query.order_by(users.year,users.g_course).all()

    picked_user = 'george'
    return render_template("index.html", matches=matches, user=picked_user)

@app.route("/mike")
def mike():

    matches = users.query.order_by(users.year,users.g_course).all()

    picked_user = 'mike'
    return render_template("index.html", matches=matches, user=picked_user)

class SelectUserForm(FlaskForm):
    picked_user = StringField("Pick a user: (george or mike)")
    submit = SubmitField("Done")

@app.route("/user", methods=['GET', 'POST'])
def pick_user():
    
    form = SelectUserForm()
    matches = users.query.order_by(users.year,users.g_course).all()
    picked_user = 'george'
    if form.validate_on_submit():
        picked_user = str(form.picked_user.data)
        return redirect(url_for('home'))
    return render_template("edit.html", matches=matches, user=picked_user, form=form)

class EditMatchForm(FlaskForm):
    search_name = StringField("Your Course Name")
    search_city = StringField("City")
    search_State = StringField("State")
    search_Country = StringField("Country")
    submit = SubmitField("Done")

@app.route("/edit", methods=['GET', 'POST'])
def edit_match():
    form = EditMatchForm()
    match_id = request.args.get("id")
    match_edit = users.query.get(match_id)
    
    if form.validate_on_submit():
        # movie.rating = float(form.rating.data)
        # movie.review = form.review.data
        # db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", match_edit=match_edit, form=form)

class AddMoviesForm(FlaskForm):
    movie_to_seach = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

@app.route("/map", methods=['GET', 'POST'])
def show_map():
    # form = AddMoviesForm()
    # if form.validate_on_submit():
    #     movie_to_search = form.movie_to_seach.data
    #     response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": creds.MOVIE_DB_API_KEY, "query": movie_to_search})
    #     data = response.json()["results"]
    #     return render_template("select.html", options=data)
    # all_movies = Movie.query.order_by(Movie.rating).all()
    # return render_template("add.html", all_movies=all_movies, form=form)
    return render_template('George_Mike_test.html')

@app.route("/find")
def find_movie():
    # movie_api_id = request.args.get("id")
    # if movie_api_id:
    #     movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
    #     response = requests.get(movie_api_url, params={"api_key": creds.MOVIE_DB_API_KEY, "language": "en-US"})
    #     data = response.json()
    #     new_movie = Movie(
    #         title=data["title"],
    #         year=data["release_date"].split("-")[0],
    #         img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
    #         description=data["overview"],

    #     )
    #     db.session.add(new_movie)
    #     db.session.commit()
        return redirect(url_for("rate_movie", id=new_movie.id))

@app.route("/delete")
def delete_movie():
    # movie_id = request.args.get("id")
    # movie = Movie.query.get(movie_id)
    # db.session.delete(movie)
    # db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

