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

