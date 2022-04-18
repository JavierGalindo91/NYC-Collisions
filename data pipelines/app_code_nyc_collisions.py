# Application code for NYC Collisions Project
from pprint import pprint
import sys
import pandas as pd, datetime
import boto3
from io import BytesIO
from sodapy  import Socrata
from secrets import app_token, access_key, secret_access_key
import pandas as pd, requests
from secrets import arc_gis_APP_TOKEN

############# PHASE 1: DATA EXTRACTION #############

# Connecting to Socrata API
data_url = 'data.cityofnewyork.us'
socrata_app_token = app_token
socrata_client = Socrata(data_url, socrata_app_token)
crash_data_set = 'h9gi-nx95'

### Setup functions for daily data extraction

# Connecting to S3
client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
s3_client = client

# Retrieve latest date from the last record uploaded to S3 bucket
# we will retrieve all the collions records starting from this date 
def list_folders(s3_client, bucket_name, key_name):

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=key_name)
    last_date_in_folder = []

    # Iterating through the pages of the collisions/ folder
    for page in pages:
        last_date_in_folder.append(page['Contents'][-1]['Key'].split("/")[1])

    return last_date_in_folder

last_date = list_folders(s3_client, 'nyc-application-collisions', 'collisions/')[-1]

print (f'Latest record uploaded to S3: {last_date}')

# Loaind list of Boroughs/Districts using nycBorough.csv file from S3
bucket_name = 'nyc-application-collisions'
file_name = 'collisions_raw_data/raw_data/nycBorough.csv'
nyc_borough = s3_client.get_object(Bucket= bucket_name, Key= file_name) 
nyc_borough = pd.read_csv(nyc_borough['Body'], header=[0])
nyc_borough.rename(columns=nyc_borough.iloc[0]).drop(nyc_borough.index[0])

# Make call to Socrata API to retrieve data between latest date recorded to current date
def get_api_data_updated(dataset, date):
    start = 0 
    chunk_size = 3000
    results = []

    current_day = str(datetime.datetime.now().strftime("%Y-%m-%d")) + "T" + str(datetime.datetime.now().strftime("%H:%M:%S"))
    date = str(date) + "T00:00:00"

    record_count = socrata_client.get(dataset, select="COUNT(*)")

    while True:
        results.extend(socrata_client.get(dataset, where=str("crash_date between '%s' and '%s'") % (date, current_day), offset=start, limit=chunk_size))
        start = start + chunk_size
        if (start > int(record_count[0]['COUNT']) ):
            break

    df = pd.DataFrame.from_records(results)
    return df

### Raw data from Socrata API
crash_df = get_api_data_updated(crash_data_set, last_date)

# If we receive an empty request from the Socrata API we will exit the script
if len(crash_df)==0:
    sys.exit()
else:
    pass

############# PHASE 2: DATA TRANSFORMATION  #############

# Get list of sorted dates from Socrata API raw data

def folder_by_date(dataset):
    dataset = dataset.sort_values(by="crash_date")
    dataset['crash_date'] = pd.to_datetime(dataset['crash_date']).dt.strftime("%Y-%m-%d")
    dates= dataset['crash_date'].drop_duplicates()
    return dates.values.tolist()

dates = folder_by_date(crash_df)

# Feed this list to the clean_collision_dataset function
# ArcGIS REST API service used to fill in missing zip codes using lon/lat coordinates in raw data
def clean_collision_dataset(dataset, date):
    dataset['crash_date'] = pd.to_datetime(dataset['crash_date']).dt.strftime("%Y-%m-%d")
    dataset = dataset[dataset['crash_date']==date]
    df = dataset.copy()

    columns = ['collision_id','crash_date','crash_time','zip_code','latitude','longitude',
    'number_of_persons_injured','number_of_persons_killed','number_of_pedestrians_injured','number_of_pedestrians_killed',
    'number_of_cyclist_injured','number_of_cyclist_killed','number_of_motorist_injured','number_of_motorist_killed',
    'contributing_factor_vehicle_1','contributing_factor_vehicle_2','vehicle_type_code1','vehicle_type_code2']

    df = df[columns]

    # Filling up the empty zipcodes using the ARCGIS API
    for index, row in df['latitude'].iteritems():
        if pd.notnull(row):
            # Skipping zipcodes we already have
            if pd.notnull(df['zip_code'][float(index)]):
                pass
            else:
                try:
                    # Making a call to the ArcGIS API to retrieve zipcode based on lon/lat coordinate
                    longitude =float(df['longitude'][float(index)])
                    latitude = float(df['latitude'][float(index)])
                    response = requests.get(f"https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={longitude},{latitude}&f=json&token={arc_gis_APP_TOKEN}&forStorage=true")
                    response_data = response.json()
                    df.loc[index, 'zip_code'] = response_data['address']['Postal']
                    
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
    df = df.drop_duplicates()
    return df

def getBorough(df1, df2, field):
    df1[field] =  df1[field].astype(str)
    df2[field] =  df2[field].astype(str)
    df = pd.merge(df1,df2,on=field)
    df = df.drop_duplicates()
    return pd.merge(df1,df2,on=field)

############# PHASE 3: DATA UPLOAD TO S3  #############

bucket_name = "nyc-application-collisions"
key_name = "collisions/"
  
# Creating a csv file for all accidents recorded in each individual date
for date in dates:
    file_name = str(date) + ".csv"
    individual_date_crash_df = clean_collision_dataset(crash_df,str(date))
    individual_date_crash_df = getBorough(individual_date_crash_df, nyc_borough, 'zip_code')
    individual_date_crash_df['crash_date#Borough'] = individual_date_crash_df['crash_date'].astype(str) + individual_date_crash_df['Boroughs']
    individual_date_crash_df= individual_date_crash_df.drop_duplicates()
    csv_buffer = BytesIO()
    #individual_date_crash_df.to_csv(str(date) +".csv", encoding='utf-8', index=False)
    individual_date_crash_df.to_csv(csv_buffer)
    content = csv_buffer.getvalue()
    folder = key_name + str(date) +"/" + file_name
    client.put_object(Bucket=bucket_name, Key=(folder), Body=content) #Creating individual date folder i.e. collisions/2012-07-01/
   
