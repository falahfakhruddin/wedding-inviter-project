# IMPORT LIBRARY
import arcgis
import pandas as pd
from arcgis.gis import GIS
from arcgis.features import GeoAccessor

# CRED, BIARIN AJA HARDCODE WKWK
user = "nanaufal"
passwd = "Nanaufal2808"

gis = GIS("https://nanaufal.maps.arcgis.com/home",
          username=user,
          password=passwd)

###### GANTI DF YANG DISINI #####
csv_input = r'D:\Non-Project\grid_view.csv'
df_input = pd.read_csv(csv_input)
#################################

# DROP DUPLICATE
df_clean = df_input.drop_duplicates("GuestName")
df_clean = df_clean.reset_index(drop=True)

# GET EXISTING RECORD
rsvp_id = 'f492f0937d99405982cb5199fd3eb2eb'
search_list = gis.content.search(rsvp_id)
portal_item = search_list[0]
table = portal_item.tables[0]
rsvp_target_df = table.query(where="1=1", as_df=True)

# JOIN TO GET NEW DATA ONLY
df_join = pd.merge(df_clean, rsvp_target_df, left_on=['GuestName'], right_on=['GuestName'], how='left')
df_join['Confirmation_y'] = df_join['Confirmation_y'].fillna("0")
df_join['Message_x'] = df_join['Message_x'].fillna("No Message")
df_join = df_join.loc[df_join['Confirmation_y'] == "0"]
df_join = df_join.reset_index(drop=True)

# PUSH NEW DATA TO TABLE
if (len(df_join) > 0):
    for i in range(len(df_join)):
        GuestName = df_join.loc[i, 'GuestName']
        Confirmation = df_join.loc[i, 'Confirmation_x']
        Confirmed = df_join.loc[i, 'Confirmed_x']
        Group = df_join.loc[i, 'Group']
        GuestFrom = df_join.loc[i, 'GuestFrom_x']
        Message = df_join.loc[i, 'Message_x']

        add_rsvp = [{"attributes": {
            'GuestName': GuestName,
            'Confirmation': Confirmation,
            'Confirmed': Confirmed,
            'Group': Group,
            'GuestFrom': GuestFrom,
            'Message': Message}}]
        print(add_rsvp)
        adding_data = table.edit_features(adds=add_rsvp, rollback_on_failure=False)
else:
    print("No new RSVP")



