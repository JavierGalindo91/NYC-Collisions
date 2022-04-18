# File that transforms the collisions raw data retrieved from the Open NYC Data API
# into individual files for each individual date worth crashes
import pandas as pd, os, requests
from secrets import arc_gis_user, arc_gis_pwd, arc_gis_APP_TOKEN
from arcgis.gis import GIS

# arcGIS
gis = GIS("http://www.arcgis.com", arc_gis_user, arc_gis_pwd)

# Function for data cleaning and transformation
def clean_collision_dataset(dataset, date):
    dataset['crash_date'] = pd.to_datetime(dataset['crash_date']).dt.strftime("%Y-%m-%d")
    dataset = dataset[dataset['crash_date']==date]
    df = dataset.copy()

    columns = ['collision_id','crash_date','crash_time','zip_code','latitude','longitude',
    'number_of_persons_injured','number_of_persons_killed','number_of_pedestrians_injured','number_of_pedestrians_killed',
    'number_of_cyclist_injured','number_of_cyclist_killed','number_of_motorist_injured','number_of_motorist_killed',
    'contributing_factor_vehicle_1','contributing_factor_vehicle_2','vehicle_type_code1','vehicle_type_code2']

    df = df[columns]
    df['Borough'] = ""

    # Filling up the empty zipcodes using the ARCGIS API
    for index, row in df['latitude'].iteritems():
        if pd.notnull(row):
            # Skipping zipcodes we already have
            if pd.notnull(df['zip_code'][float(index)]):
                #print ("Skipping row %s, lon: %s, lat: %s" %(index, df['longitude'][float(index)], df['latitude'][float(index)]) )
                pass
            else:
                try:
                    #Create a tuple to feed into the point
                    longitude =float(df['longitude'][float(index)])
                    latitude = float(df['latitude'][float(index)])
                    response = requests.get(f"https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={longitude},{latitude}&f=json&token={arc_gis_APP_TOKEN}&forStorage=true")
                    response_data = response.json()
                    df.loc[index, 'zip_code'] = response_data['address']['Postal']
                    df.loc[index, 'Borough'] = response_data['address']['District']
                    
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print (message)
        else:
            pass
    
    df = df[~df['zip_code'].isnull()]
    df = df[~df['collision_id'].isnull()]
    df[columns] = df[columns].fillna('Unspecified')
    print ("Completed record for date: %s" %(date))
    return df

# Retrieve crash and borough data from local directory
# TO-DO Look for a way to extract raw file from S3
crash_df = pd.read_csv("collisions_raw_data.csv", header=[0])
#crash_df = crash_df.iloc[0:10]
nyc_borough = pd.read_csv("nycBorough.csv", header=[0])
nyc_borough.rename(columns=nyc_borough.iloc[0]).drop(nyc_borough.index[0])

def getBorough(df1, df2, field):
    df1[field] =  df1[field].astype(str)
    df2[field] =  df2[field].astype(str)
    return pd.merge(df1,df2,on=field)

# Getting list of sorted dates 
def folder_by_date(dataset):
    dataset = dataset.sort_values(by="crash_date")
    dataset['crash_date'] = pd.to_datetime(dataset['crash_date']).dt.strftime("%Y-%m-%d")
    dates= dataset['crash_date'].drop_duplicates()
    return dates.values.tolist()

dates = folder_by_date(crash_df)

# Cleaning data by individual date and saving locally
for date in dates:
    os.chdir(r'C:\Users\javie\OneDrive\Documents\NYC_Data_Engineer_Project\collisions_data')
    path = date + ".csv"

    if os.path.exists(path):
        pass
    else:
        individual_crash_df = clean_collision_dataset(crash_df,str(date))
        individual_crash_df = getBorough(individual_crash_df, nyc_borough, 'zip_code')
        individual_crash_df['crash_date#Borough'] = individual_crash_df['crash_date'].astype(str) + individual_crash_df['Boroughs']
        individual_crash_df.to_csv(str(date) +".csv", encoding='utf-8', index=False)
        
