import pandas as pd
import folium
import sqlite3
import fuzzymatcher

cnx = sqlite3.connect('garmin.db')

df_all_courses = pd.read_sql_query("SELECT * FROM courses", cnx)

df_george_raw = pd.read_csv ('george_courses.csv')

g_left = ["Course", "City", "State"]
db_right = ["name", "city", "state"]
# fuzzy_match = fuzzymatcher.fuzzy_left_join(df_george_raw, df_all_courses, g_left, db_right)
# fuzzy_match.to_csv('george_fuzzy_match.csv')

dfm = pd.read_csv('george_fuzzy_match.csv')
print(dfm)
courses_to_map = []
for i in dfm.itertuples():
    if i[2] < .2:
         print(f"index {i[0]}, course: {i[5]}, match score: {i[2]}")  # list bad matches
    if i[2] > .2:
        c = {
            'course':i[11].lstrip(),
            'lat':i[16],
            'long':i[17]
        }
        courses_to_map.append(c)

test_index = int(input("Which index to see matches? "))
print(df_george_raw)
test_df = df_george_raw.loc[[test_index]] 
print(test_df)
single_match = fuzzymatcher.fuzzy_left_join(test_df, df_all_courses, g_left, db_right)
cols = db_right = ["best_match_score", "name", "city", "state"]
rearranged_best_matches=single_match[cols].sort_values(by=['best_match_score'], ascending=False)
print(rearranged_best_matches.head(5))

# cm = dfm[["name","latitude","longitude", "best_match_score"]]
# map = folium.Map(location=[cm.latitude.mean(), cm.longitude.mean()], zoom_start=3, control_scale=True)
# fg = folium.FeatureGroup(name="George")
# for i in courses_to_map:
#     fg.add_child(folium.CircleMarker(location=[i['lat'],i['long']], popup=i['course']))
# map.add_child(fg)
# map.save("George_test.html")

