# File that extracts the entire collisions dataset from the Socrata API
import pandas as pd, datetime
import boto3
from sodapy  import Socrata
from secrets import app_token, access_key, secret_access_key

# socrata api
data_url = 'data.cityofnewyork.us'
app_token = app_token
socrata_client = Socrata(data_url, app_token)
crash_data_set = 'h9gi-nx95'

# This function retrieves the entire dataset from the API - All records starting 2012
def get_api_data(dataset):
    start = 0 
    chunk_size = 3000
    results = []

    record_count = socrata_client.get(dataset, select="COUNT(*)")

    while True:
        results.extend(socrata_client.get(dataset, offset=start, limit=chunk_size))
        start = start + chunk_size
        if (start > int(record_count[0]['COUNT']) ):
            break

    df = pd.DataFrame.from_records(results)
    return df

# For new daily files:
# 1. We are going to take the latest date from the name of the latest csv file uploaded in the collisions/ folder in S3
# 2. We are making a call to the API to retrieve data between this last date until today

# Getting latest date from S3
client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

def list_folders(s3_client, bucket_name, key_name):

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=key_name)
    last_date_in_folder = []

    # Iteration through the pages of the collisions/ folder
    for page in pages:
        last_date_in_folder.append(page['Contents'][-1]['Key'].split("/")[1])

    return last_date_in_folder

s3_client = client
last_date = list_folders(s3_client, 'nyc-application-collisions', 'collisions/')[-1]

# Function that makes the API call using the lastest date the collisions/ folder in S3
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

# Saving the API data for the most recent call
crash_df = get_api_data_updated(crash_data_set, last_date)
crash_df.to_csv(f"collisions_raw_data_{last_date}.csv", encoding='utf-8', index=False)
