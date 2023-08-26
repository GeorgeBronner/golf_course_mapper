import os
import pandas as pd
import folium
import sqlite3
import fuzzymatcher

def make_map():
    basedir = os.path.abspath(os.path.dirname(__file__))
    cnx = sqlite3.connect(os.path.join(basedir, "garmin.db"))
    # cnx = sqlite3.connect('garmin.db')

    df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

    df_matches = pd.read_sql_query("SELECT * FROM users", cnx)

    def load_feature_group(dfm):
        courses_to_map = []
        for i in dfm.itertuples():
            print(i)
            id = i[1] - 1 # get the id from the garmin list and subtract 1 to match with dataframe index
            print(f"id= {i[1]}")

            c = {
                'course':df_all_courses.loc[id]['g_course'],
                'lat':df_all_courses.loc[id]['g_latitude'],
                'long':df_all_courses.loc[id]['g_longitude'],
                'id':id
            }
            print(c)
            courses_to_map.append(c)
        fg = folium.FeatureGroup(name=f"ALL")
        for i in courses_to_map:
            new_description = i['course'] + ' ' + str(i['id'] + 1)
            fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description, color='green', opacity=0.7, radius=7))
        map.add_child(fg)
        return

    # cm = df_matches[["g_course","latitude","longitude", "best_match_score"]]
    map = folium.Map(location=[40, -90], zoom_start=4, control_scale=True)
    # map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)

    load_feature_group(df_all_courses)
    map.add_child(folium.LayerControl())

    map.save("templates/folium_map_all.html")

if __name__ == '__main__':
    make_map()