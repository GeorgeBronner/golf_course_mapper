import os
import sys
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox742ssdfgKR6b'
Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "garmin.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    g_course = db.Column(db.String(250))
    g_address = db.Column(db.String(250))
    g_city = db.Column(db.String(100))
    g_state = db.Column(db.String(40))
    g_country = db.Column(db.String(40))
    g_latitude = db.Column(db.Float)
    g_longitude = db.Column(db.Float)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<course {self.g_course}>'

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
    manual_match = db.Column(db.Boolean)
    garmin_ID = db.Column(db.Integer)
    manual_course = db.Column(db.String(250))
    manual_city = db.Column(db.String(100))
    manual_state = db.Column(db.String(40))
    manual_country = db.Column(db.String(40))
    manual_latitude = db.Column(db.Float)
    manual_longitude = db.Column(db.Float)

class matches(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    id_left = db.Column(db.String(250))
    id_right = db.Column(db.String(250))
    match_score = db.Column(db.Float)
    match_rank = db.Column(db.Integer)
    g_course = db.Column(db.String(250))
    city = db.Column(db.String(250))
    g_city = db.Column(db.String(250))
    state = db.Column(db.String(250))
    g_state = db.Column(db.String(250))
    country = db.Column(db.String(250))
    course = db.Column(db.String(250))
    g_country = db.Column(db.String(250))

@app.route("/")
def home():
    garmin_courses = courses.query.all()
    user_matches = users.query.order_by(users.year,users.course).all()

    picked_user = 'george'
    return render_template("index.html", matches=user_matches, user=picked_user, garmin_courses=garmin_courses)
    # return (f"{garmin_courses[2].g_course}")

@app.route("/mike")
def mike():

    garmin_courses = courses.query.all()
    user_matches = users.query.order_by(users.year,users.course).all()

    picked_user = 'mike'
    return render_template("mike.html", matches=user_matches, user=picked_user, garmin_courses=garmin_courses)

@app.route("/top100")
def top100():

    garmin_courses = courses.query.all()
    user_matches = users.query.order_by(users.year,users.course).all()

    picked_user = 'top100'
    return render_template("top100.html", matches=user_matches, user=picked_user, garmin_courses=garmin_courses)

@app.route("/garmin_courses")
def garmin_list():

    garmin_courses = courses.query.all()

    return render_template("garmin_course_list.html", garmin=garmin_courses)

class SelectUserForm(FlaskForm):
    picked_user = StringField("Pick a user: (george or mike)")
    submit = SubmitField("Done")

# @app.route("/user", methods=['GET', 'POST'])
# def pick_user():
#     form = SelectUserForm()
#     matches = users.query.order_by(users.year,users.course).all()
#     picked_user = 'george'
#     if form.validate_on_submit():
#         picked_user = str(form.picked_user.data)
#         return redirect(url_for('home'))
#     return render_template("edit.html", matches=matches, user=picked_user, form=form)

class EditMatchForm(FlaskForm):
    manual_garmin_id = IntegerField("Manual Garmin ID")
    submit = SubmitField("Set")

@app.route("/edit", methods=['GET', 'POST'])
def edit_match():
    raw_matches = matches.query.all()
    form = EditMatchForm()
    match_id = request.args.get("id")
    match_edit = users.query.get(match_id)
    id_left = str(int(match_id) - 1) + "_left"
    
    if form.validate_on_submit():
        maunal_garmin_id = form.manual_garmin_id.data - 1
        return redirect(url_for('confirmAuto',id=maunal_garmin_id, id_left=id_left))
    return render_template("edit.html", match_edit=match_edit, raw_matches=raw_matches, form=form, id_left=id_left, match_id=match_id)

@app.route("/confirm-auto", methods=['GET', 'POST'])
def confirmAuto():
    form = EditMatchForm()
    garmin_id = request.args.get("id") 
    garmin_id = int(garmin_id.split("_")[0]) + 1
    course_to_edit_id = request.args.get("id_left")
    course_to_edit_id = int(course_to_edit_id.split("_")[0]) + 1
    garmin_course = courses.query.get(garmin_id)
    print(garmin_id)
    match_edit = users.query.get(course_to_edit_id)
    
    # if form.validate_on_submit():
    #     # movie.rating = float(form.rating.data)
    #     # movie.review = form.review.data
    #     # db.session.commit()
    #     return redirect(url_for('home'))
    return render_template("confirm-auto.html", match_edit=match_edit, form=form, garmin_course=garmin_course, match_id=course_to_edit_id)    

@app.route("/update_success", methods=['GET', 'POST'])
def updateSuccess():
    garmin_id = request.args.get("garmin_id")
    # garmin_id = int(garmin_id.split("_")[0]) + 1
    course_to_edit_id = request.args.get("match_id")
    # course_to_edit_id = int(course_to_edit_id.split("_")[0]) + 1
    garmin_course = courses.query.get(garmin_id)
    # print(garmin_course)
    match_edit = users.query.get(course_to_edit_id)
    print(f'The garmin id is: {garmin_id} and the type is {type(garmin_id)}', file=sys.stdout)
    match_edit.garmin_ID = int(garmin_id)
    match_edit.good_match = 1
    db.session.commit()
    import map
    map.make_map()

    # if form.validate_on_submit():
    #     # movie.rating = float(form.rating.data)
    #     # movie.review = form.review.data
    #     # db.session.commit()
    #     return redirect(url_for('home'))
    return render_template("update-success.html", garmin_course=garmin_course, match_edit=match_edit)    


@app.route("/map", methods=['GET', 'POST'])
def show_map():

    # return render_template('George_Mike_test.html')
    return render_template('show_map.html')

@app.route("/fullmap", methods=['GET', 'POST'])
def show_full_map():

    return render_template('folium_map.html')

@app.route("/all", methods=['GET', 'POST'])
def show_all_map():

    return render_template('folium_map_all.html')

@app.route("/find")
def find_movie():
    form = EditMatchForm()
    match_id = request.args.get("id")
    match_edit = users.query.get(match_id)
    
    
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
    return redirect(url_for("rate_movie", match_edit=match_edit))

class AddCourseForm(FlaskForm):
    user = SelectField("User", choices=['george','mike'], validators=[DataRequired()])
    course = StringField("Course", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    year = IntegerField("Year")
    submit = SubmitField("Add Course")

@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        new_course = users(user=form.user.data, course=form.course.data, city=form.city.data,
                         state=form.state.data, country=form.country.data, year=form.year.data)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_course.html", form=form)

class DeleteUserCourse(FlaskForm):
    submit = SubmitField("Delete")

@app.route("/delete", methods=["GET", "POST"])
def delete_user_course():
    form = DeleteUserCourse()
    delete_id = request.args.get("id")
    delete_course = users.query.get(delete_id)
    if form.validate_on_submit():
        
        db.session.delete(delete_course)
        db.session.commit()
        import map
        map.make_map()
        return redirect(url_for("home"))
    return render_template("delete_user_course.html", form=form, course=delete_course)

class AddGarminCourseForm(FlaskForm):
    course = StringField("Course Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[DataRequired()])
    longitude = FloatField("Longitude", validators=[DataRequired()])
    submit = SubmitField("Add Course")

@app.route("/add_garmin_course", methods=["GET", "POST"])
def add_garmin_course():
    form = AddGarminCourseForm()
    if form.validate_on_submit():
        new_course = courses(g_course=form.course.data, g_address=form.address.data, g_city=form.city.data,
                         g_state=form.state.data, g_country=form.country.data, g_latitude=form.latitude.data, 
                         g_longitude=form.longitude.data)

        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_garmin_course.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)

