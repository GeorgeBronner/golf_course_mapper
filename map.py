import pandas as pd
import folium
import sqlite3
import fuzzymatcher

def make_map():
    cnx = sqlite3.connect('garmin.db')

    df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

    df_matches = pd.read_sql_query("SELECT * FROM users", cnx)

    def load_feature_group(dfm, name, color):
        courses_to_map = []
        for i in dfm.itertuples():
            id = i[11] - 1 # get the id from the gamrin list and subtract 1 to match with dataframe index
            print(f"id= {i[11]}")
            if i[2] != name:
                print(f"name= {name}")
                continue
            if not i[9]:
                print(f"i[9]= is {i[9]}")
                print(f"course: {i[3]}, match score: {i[8]}")  # list bad matches
            else :
                c = {
                    'course':df_all_courses.loc[id]['g_course'],
                    'lat':df_all_courses.loc[id]['g_latitude'],
                    'long':df_all_courses.loc[id]['g_longitude'],
                    'id':id
                }
                print(c)
                courses_to_map.append(c)
        fg = folium.FeatureGroup(name=f"{name}")
        for i in courses_to_map:
            new_description = i['course'] + ' ' + str(i['id'] + 1)
            fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=new_description, color=color, opacity=0.7, radius=7))
        map.add_child(fg)
        return

    # cm = df_matches[["g_course","latitude","longitude", "best_match_score"]]
    map = folium.Map(location=[40, -90], zoom_start=4, control_scale=True)
    # map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)

    load_feature_group(df_matches, "george", 'red')
    load_feature_group(df_matches, "mike", 'blue')
    map.add_child(folium.LayerControl())

    map.save("templates/George_Mike_test.html")

if __name__ == '__main__':
    make_map()