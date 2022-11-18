from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
engine = create_engine('sqlite:///garmin.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    g_course = Column(String(250))
    g_address = Column(String(250))
    g_city = Column(String(100))
    g_state = Column(String(40))
    g_country = Column(String(40))
    g_latitude = Column(Float)
    g_longitude = Column(Float)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
result = int(input(f"Which course id to you want to edit? "))
i = session.query(courses).get(result)
    
print(f'Course: {i.g_course}, city: {i.g_city}, country: {i.g_country}, id: {i.id}')
result = input("Is this the course you want to edit? ")
if result == 'y':
    new_lat = float(input('Enter Latitude: '))
    new_long = float(input('Enter Longitude: '))
    confirm = input(f'Do you want to update Course: {i.g_course}, city: {i.g_city}, country: {i.g_country}, id: {i.id}, with lat: {new_lat}, long={new_long} ? ')
    if confirm == 'y':
        i.g_latitude = new_lat
        i.g_longitude = new_long
        session.commit()
else:
    pass
    
# for i in courses:   # to remove leading spaces
#     i.name = i.name.replace("~","-")
#     print(f'now my name is:{i.name}')
# db.session.commit()
