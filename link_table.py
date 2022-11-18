import pandas as pd
import sqlite3
import fuzzymatcher

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Boolean
engine = create_engine('sqlite:///garmin.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class link_table(Base):
    __tablename__ = 'link_table'
    index_label = Column(Integer, primary_key=True)
    user = Column(String(250))
    course = Column(String(250))
    city = Column(String(100))
    state = Column(String(40))
    country = Column(String(40))
    year = Column(Integer)
    match_score = Column(Float)
    good_match = Column(Boolean)
    manual_match = Column(Boolean)
    garmin_ID = Column(String(100))
    g_course = Column(String(250))
    g_city = Column(String(100))
    g_state = Column(String(40))
    g_country = Column(String(40))


# Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
# result = session.query(courses).all()



cnx = sqlite3.connect('garmin.db')
df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

df_all = pd.read_sql_query("SELECT * FROM users", cnx)
df_all = df_all.drop(df_all.columns[[7,10,11,12,13,14,15,16]], axis=1)

g_left = ["course", "city", "state", "country"]
db_right = ["g_course", "g_city", "g_state", "g_country"]

fuzzy_table = fuzzymatcher.link_table(df_all, df_all_courses, g_left, db_right)
fuzzy_table = fuzzy_table[fuzzy_table['match_rank'] < 6]
fuzzy_table.to_csv("match_table.csv")
