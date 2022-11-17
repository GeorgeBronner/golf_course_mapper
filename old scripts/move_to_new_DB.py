import pandas as pd
import sqlite3
import fuzzymatcher

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Boolean
engine = create_engine('sqlite:///garmin.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class courses2(Base):
    __tablename__ = 'courses2'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    city = Column(String(100))
    state = Column(String(40))
    country = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)

# Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session2 = Session()

import folium
import requests, json
import time


from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///garmin.db"
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

courses = db.session.query(courses).all()
for i in courses:
    new_course = courses2(
        name = i.name,
        address = i.address,
        city = i.city,
        state = i.state,
        country = i.country,
        latitude = i.latitude,
        longitude = i.longitude,
    )
    session2.add(new_course)
session2.commit()
# cnx = sqlite3.connect('garmin.db')

# df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

# # df_george_raw = pd.read_csv ('george_courses.csv')

# df_george_raw = pd.read_csv ('mike_courses.csv')


# g_left = ["Course", "City1", "State1"]
# db_right = ["name", "city", "state"]
# fuzzy_match = fuzzymatcher.fuzzy_left_join(df_george_raw, df_all_courses, g_left, db_right)
# for i in fuzzy_match.itertuples():

#     # print(f'course = {i[4]}, city = {i[5]}, state = {i[6]}, country = {i[7]}, year = {i[8]}, 
#     #     best_match_score = {i[1]}, good_match = {a_good_match}, garmin_ID = {i[9]}, 
#     #     g_course = {i[10]}, g_city = {i[11]}, g_state = {i[12]}, g_country = {i[13]}, 
#     #     latitude = {i[14]}, longitude = {i[15]}')
    
#     if i[1] > .3:
#         a_good_match = True
#     else:
#         a_good_match = False
#     new_match = users(
#         user = 'mike',
#         course = i[4],
#         city = i[5],
#         state = i[6],
#         country = i[7],
#         year = i[8],
#         best_match_score = i[1],
#         good_match = a_good_match,
#         garmin_ID = i[9],
#         g_course = i[10],
#         g_city = i[12],
#         g_state = i[13],
#         g_country = i[14],
#         latitude = i[15],
#         longitude = i[16],
#     )
#     session.add(new_match)
#     session.commit()

# # fuzzy_match.to_sql(name='george', con=cnx)
# # cnx.close()

# # fuzzy_match.to_csv('george_fuzzy_match.csv')

# # dfm = pd.read_csv('george_fuzzy_match.csv')
# # print(dfm)
# # courses_to_map = []
# # for i in dfm.itertuples():
# #     if i[2] < .2:
# #          print(f"course: {i[5]}, match score: {i[2]}")  # list bad matches
# #     if i[2] > .2:
# #         c = {
# #             'course':i[11].lstrip(),
# #             'lat':i[16],
# #             'long':i[17],
# #             'id':i[10]
# #         }
# #         courses_to_map.append(c)

# # cm = dfm[["name","latitude","longitude", "best_match_score"]]
# # map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)
# # fg = folium.FeatureGroup(name="George")
# # for i in courses_to_map:
# #     new_description = i['course'] + ' ' + str(i['id'])
# #     fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description))
# # map.add_child(fg)
# # map.save("George_test.html")

