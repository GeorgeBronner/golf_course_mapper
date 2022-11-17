from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
engine = create_engine('sqlite:///garmin.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    city = Column(String(100))
    state = Column(String(40))
    country = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
result = session.query(courses).all()
    
for i in result:
    if i.id == 48:
        print(f'Course: {i.name}, city: {i.city}, country: {i.country}, id: {i.id}')
        new_lat = float(input('Enter Latitude: '))
        new_long = float(input('Enter Longitude: '))
        confirm = input(f'Do you want to update Course: {i.name}, city: {i.city}, country: {i.country}, id: {i.id}, with lat: {new_lat}, long={new_long} ? ')
        if confirm == 'y':
            i.latitude = new_lat
            i.longitude = new_long
            session.commit()
            break
    
# for i in courses:   # to remove leading spaces
#     i.name = i.name.replace("~","-")
#     print(f'now my name is:{i.name}')
# db.session.commit()
