import pandas as pd
import folium
import sqlite3
import fuzzymatcher


cnx = sqlite3.connect('garmin.db')

df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

df_matches = pd.read_sql_query("SELECT * FROM users", cnx)

def load_feature_group(dfm, name, color):
    courses_to_map = []
    for i in dfm.itertuples():
        if i[2] != name:
            continue
        if not i[9]:
             print(f"course: {i[3]}, match score: {i[8]}")  # list bad matches
        else :
            c = {
                'course':i[11],
                'lat':i[15],
                'long':i[16],
                'id':i[10]
            }
            courses_to_map.append(c)
    fg = folium.FeatureGroup(name=f"{name}")
    for i in courses_to_map:
        new_description = i['course'] + ' ' + str(i['id'])
        fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description, color=color, opacity=0.7))
    map.add_child(fg)
    return

cm = df_matches[["g_course","latitude","longitude", "best_match_score"]]
map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)

load_feature_group(df_matches, "george", 'red')
load_feature_group(df_matches, "mike", 'blue')
map.add_child(folium.LayerControl())

map.save("templates/George_Mike_test.html")

