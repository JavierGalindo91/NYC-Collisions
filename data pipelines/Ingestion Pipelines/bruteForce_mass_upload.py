import time
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from sodapy import Socrata
from secrets_1 import app_token, access_key, secret_access_key

def get_api_records(client, api_url, app_token, dataset_name):
    """
    Fetches records from Socrata API endpoint in chunks and returns them as a DataFrame.

    Args:
        client (sodapy.Socrata): The Socrata client for making API requests.
        api_url (str): The URL of the API endpoint.
        app_token (str): The application token for accessing the API.
        dataset_name (str): The name of the dataset to retrieve.

    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved records.
    """
    start = 0 
    chunk_size = 5000
    client.timeout = 100
    results =[]
    number_of_requests_sent = 0 
    
    # Retrieve the total record count
    record_count = client.get(dataset_name, select="COUNT(*)")
    total_records = int(record_count[0]['COUNT'])


    # Get the data in chunks of 5,000 records 
    while True:
        results.extend(client.get(dataset_name, offset=start, limit=chunk_size, order='collision_id'))
        start += chunk_size
        if (start > total_records):
            break
        number_of_requests_sent += 1
    
    print("BRUTE FORCE APPROACH")
    print(f"Total number of records: {total_records}")
    print(f'Number of requests sent {number_of_requests_sent}')
    
    return pd.DataFrame.from_records(results)
    

def upload_dataframe_to_s3(client, bucket_name, key_name, df, dataset_name):
    """
    Uploads a DataFrame to an S3 bucket using the provided AWS S3 client.

    Args:
        client (boto3.client): An AWS S3 client object.
        bucket_name (str): The name of the S3 bucket.
        key_name (str): The key (object name) under which the data will be stored in the S3 bucket.
        df (pandas.DataFrame): The DataFrame to upload.
        dataset_name (str): The name of the dataset being uploaded.

    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    
    csv_buffer = df.to_csv(index=False)

    try:
        # Upload the CSV file to S3
        client.put_object(Bucket=bucket_name, Key=key_name, Body=csv_buffer.encode('utf-8'))
        print(f"Uploaded '{dataset_name}' to '{bucket_name}/{key_name}' successfully.")
        return True
    except ClientError as e:
        print(f"Error uploading '{dataset_name}' to '{bucket_name}/{key_name}': {e}")
        return False


# TRYING THE BRUTE FORCE APPROACH FOR MASS UPLOAD
def main():
    data_url = 'data.cityofnewyork.us'
    socrata_client = Socrata(data_url, app_token)
    crash_data_set = 'h9gi-nx95'
    bucket_name = 'nyc-application-collisions'
    key_name = 'collisions_raw_data'

    # Measure execution time
    start_time = time.time()

    # Call on Brute Force Method for Mass Download
    crash_df = get_api_records(socrata_client, data_url, app_token, crash_data_set)

    # Connect to AWS boto3 client - Make sure to check the security settings 
    aws_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

    # Upload directly to S3 collisions_raw_data key
    upload_dataframe_to_s3(aws_client, bucket_name, key_name+"/'crash_data_set_bfc.csv'", crash_df, 'crash_data_set_bfc.csv')

    # Calculate and print execution time
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds\n")

if __name__ == '__main__':
    main()
