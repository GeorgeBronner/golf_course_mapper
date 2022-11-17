import pandas as pd
import folium
import sqlite3
import fuzzymatcher

cnx = sqlite3.connect('garmin.db')
df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

df_mike_raw = pd.read_csv ('mike_courses.csv')


g_left = ["Course", "City", "State"]
db_right = ["name", "city", "state"]
fuzzy_match = fuzzymatcher.fuzzy_left_join(df_mike_raw, df_all_courses, g_left, db_right)
fuzzy_match.to_csv('mike_fuzzy_match.csv')

dfm = pd.read_csv('mike_fuzzy_match.csv')
print(dfm)
courses_to_map = []
for i in dfm.itertuples():
    if i[2] < .2:
         print(f"course: {i[5]}, match score: {i[2]}")  # list bad matches
    if i[2] > .2:
        c = {
            'course':i[11].lstrip(),
            'lat':i[16],
            'long':i[17],
            'id':i[10]
        }
        courses_to_map.append(c)

cm = dfm[["name","latitude","longitude", "best_match_score"]]
map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)
fg = folium.FeatureGroup(name="Mike")
for i in courses_to_map:
    new_description = i['course'] + ' ' + str(i['id'])
    fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description))

map.add_child(fg)
map.save("Mike_test.html")

