import pandas as pd
import sqlite3
import fuzzymatcher

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Boolean
engine = create_engine('sqlite:///garmin.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class users(Base):
    __tablename__ = 'users'
    index_label = Column(Integer, primary_key=True)
    user = Column(String(250))
    course = Column(String(250))
    city = Column(String(100))
    state = Column(String(40))
    country = Column(String(40))
    year = Column(Integer)
    best_match_score = Column(Float)
    good_match = Column(Boolean)
    manual_match = Column(Boolean)
    garmin_ID = Column(String(100))
    manual_course = Column(String(250))
    manual_city = Column(String(100))
    manual_state = Column(String(40))
    manual_country = Column(String(40))
    manual_latitude = Column(Float)
    manual_longitude = Column(Float)

# Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
# result = session.query(courses).all()



cnx = sqlite3.connect('garmin.db')

df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

df_george_raw = pd.read_csv ('george_courses.csv')

df_mike_raw = pd.read_csv ('mike_courses.csv')


g_left = ["Course", "City", "State", "Country"]
db_right = ["g_course", "g_city", "g_state", "g_country"]
fuzzy_match_george = fuzzymatcher.fuzzy_left_join(df_george_raw, df_all_courses, g_left, db_right)
for i in fuzzy_match_george.itertuples():
    
    if i[1] > .3:
        a_good_match = True
        new_match = users(
            user = 'george',
            course = i[4],
            city = i[5],
            state = i[6],
            country = i[7],
            year = i[8],
            best_match_score = i[1],
            good_match = a_good_match,
            manual_match = False,
            garmin_ID = i[9],
        )
    else:
        a_good_match = False
        new_match = users(
            user = 'george',
            course = i[4],
            city = i[5],
            state = i[6],
            country = i[7],
            year = i[8],
            best_match_score = i[1],
            good_match = a_good_match,
            manual_match = False,
            garmin_ID = i[9],
        )
    session.add(new_match)
session.commit()

fuzzy_match_mike = fuzzymatcher.fuzzy_left_join(df_mike_raw, df_all_courses, g_left, db_right)
for i in fuzzy_match_mike.itertuples():
    
    if i[1] > .3:
        a_good_match = True
        new_match = users(
            user = 'mike',
            course = i[4],
            city = i[5],
            state = i[6],
            country = i[7],
            year = i[8],
            best_match_score = i[1],
            good_match = a_good_match,
            manual_match = False,
            garmin_ID = i[9],
        )
    else:
        a_good_match = False
        new_match = users(
            user = 'mike',
            course = i[4],
            city = i[5],
            state = i[6],
            country = i[7],
            year = i[8],
            best_match_score = i[1],
            good_match = a_good_match,
            manual_match = False,
            garmin_ID = i[9],
        )
    session.add(new_match)
session.commit()

df_george_raw.append(df_mike_raw)
df_george_raw.to_csv("joined.cvs")
fuzzy_table = fuzzymatcher.link_table(df_george_raw, df_all_courses, g_left, db_right)
fuzzy_table = fuzzy_table[fuzzy_table['match_rank'] < 6]
fuzzy_table.to_csv("fuzzy_table.csv")

# fuzzy_match.to_sql(name='george', con=cnx)
# cnx.close()

# fuzzy_match.to_csv('george_fuzzy_match.csv')

# dfm = pd.read_csv('george_fuzzy_match.csv')
# print(dfm)
# courses_to_map = []
# for i in dfm.itertuples():
#     if i[2] < .2:
#          print(f"course: {i[5]}, match score: {i[2]}")  # list bad matches
#     if i[2] > .2:
#         c = {
#             'course':i[11].lstrip(),
#             'lat':i[16],
#             'long':i[17],
#             'id':i[10]
#         }
#         courses_to_map.append(c)

# cm = dfm[["name","latitude","longitude", "best_match_score"]]
# map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)
# fg = folium.FeatureGroup(name="George")
# for i in courses_to_map:
#     new_description = i['course'] + ' ' + str(i['id'])
#     fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description))
# map.add_child(fg)
# map.save("George_test.html")

