# IMPORT LIBRARY
import pandas as pd
from arcgis.gis import GIS
from pyairtable import Table
from flask import current_app as app


def construct_df_from_airtable(config_airtable):
    base_id = config_airtable["BASE_ID"] #"appOzeOyw1sSt19id"
    api_key = config_airtable["API_KEY"]  #"keyBPJ9RW4g0TQePV"
    table_name = config_airtable["TABLE_NAME"] #"Guest"

    # init connection to airtable
    table = Table(api_key, base_id, table_name)
    guest_data = table.all()

    # init dataframe
    df = pd.DataFrame({'GuestName': pd.Series(dtype='str'),
                       'Confirmation': pd.Series(dtype='str'),
                       'Confirmed': pd.Series(dtype='int'),
                       'Group': pd.Series(dtype='str'),
                       'GuestFrom': pd.Series(dtype='str'),
                       'Message': pd.Series(dtype='str')})

    # populate data guest data to dataframe
    for guest in guest_data:
        df = df.append(guest['fields'], ignore_index=True)

    return df


def upload_data_to_arcgis(config_gis, df_input):
    # CRED, BIARIN AJA HARDCODE WKWK
    user = config_gis["USER"] #"nanaufal"
    passwd = config_gis["PASS"] #"Nanaufal2808"
    url = config_gis["URL"] #"https://nanaufal.maps.arcgis.com/home"

    gis = GIS(url,
              username=user,
              password=passwd)

    # DROP DUPLICATE
    app.logger.info("drop duplicating data from df")
    df_clean = df_input.drop_duplicates("GuestName")
    df_clean = df_clean.reset_index(drop=True)

    # GET EXISTING RECORD
    app.logger.info("drop duplicating data from df")
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
            guest_name = df_join.loc[i, 'GuestName']
            confirmation = df_join.loc[i, 'Confirmation_x']
            confirmed = df_join.loc[i, 'Confirmed_x']
            group = df_join.loc[i, 'Group']
            guest_from = df_join.loc[i, 'GuestFrom_x']
            message = df_join.loc[i, 'Message_x']

            add_rsvp = [{"attributes": {
                'GuestName': guest_name,
                'Confirmation': confirmation,
                'Confirmed': confirmed,
                'Group': group,
                'GuestFrom': guest_from,
                'Message': message}}]
            app.logger.info("add rsvp: {}".format(add_rsvp))
            adding_data = table.edit_features(adds=add_rsvp, rollback_on_failure=False)
    else:
        app.logger.info("No new RSVP")
