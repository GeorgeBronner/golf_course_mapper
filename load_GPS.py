from keys import positionstack_API_KEY, locationiq_API_KEY
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

#cursor.execute("CREATE TABLE alabama (id INTEGER PRIMARY KEY, name TEXT, address_raw TEXT, address_clean TEXT)")

##CREATE TABLE
class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    address = db.Column(db.String(250))
    city = db.Column(db.String(100))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<course {self.name}>'

courses = db.session.query(courses).all()
def positionstack():
    for i in courses:

        address = i.address
        city_state_zip = i.city_state_zip
        full_address = address + ' ' + city_state_zip 
        parameters = {
            "access_key": positionstack_API_KEY,
            "query": full_address
        }
        print(f"Searching Positionstack for {i.name}, address={i.address}")
        response = requests.get(url="http://api.positionstack.com/v1/forward", params=parameters)
        response = response.json()
        # print(f"json reponse , {response}")
        a = response['data'][0]
        print(f"data[0] reponse , {a}")
        if a != []:
            i.latitude = a['latitude']
            i.longitude = a['longitude']
            db.session.commit()

def locationiq():
    for i in courses:
        if i.latitude != 0:
            continue
        time.sleep(1)
        full_address = i.address + ' ' + i.city + ' ' + i.state
        parameters = {
            "key": locationiq_API_KEY,
            "q": full_address,
            "format": "json"
        }
        print(f"Searching locationiq for id {i.id} {i.name}, address={i.address}, {i.city}, {i.state}")
        response = requests.get(url="https://us1.locationiq.com/v1/search.php", params=parameters)
        try:
            a = response.json()[0]
        except KeyError:
            continue
        print(f"[0] response.json()[0] , {a}")
        if a != []:
            i.latitude = a['lat']
            i.longitude = a['lon']
            db.session.commit()
            print(f"worked for {i.name}")

locationiq()

# a = {'data': [{'latitude': 34.297094, 'longitude': -86.199217, 'type': 'address', 'name': '860 Country Club Road', 'number': '860', 'postal_code': None, 'street': 'Country Club Road', 'confidence': 1, 'region': 'Alabama', 'region_code': 'AL', 'county': 'Marshall County', 'locality': 'Albertville', 'administrative_area': None, 'neighbourhood': None, 'country': 'United States', 'country_code': 'USA', 'continent': 'North America', 'label': '860 Country Club Road, Albertville, AL, USA', 'map_url': 'https://map.positionstack.com/export/embed.html?bbox=-86.198717,34.297594,-86.199717,34.296594&layer=mapnik&marker=34.297094,-86.199217'}]}
# b = (a['data'][0])
# print(b['latitude'])