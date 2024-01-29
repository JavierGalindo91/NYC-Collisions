import time,os
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import concurrent.futures
from sodapy import Socrata
from secrets_1 import app_token, access_key, secret_access_key

def fetch_data_chunk(offset, chunk_size, client, dataset_name):
    """
    Fetch a chunk of data from a dataset.
    
    Args:
        offset (int): The offset from where to start fetching data.
        chunk_size (int): The number of records to fetch in this chunk.
        client: The client object responsible for interacting with the dataset.
        dataset_name (str): The name of the dataset to fetch data from.

    Returns:
        list: A list of records retrieved from the dataset.

    Example:
        To fetch the first 100 records from a dataset named 'my_dataset', you can call:
        fetch_data_chunk(0, 100, my_client, 'my_dataset')
    """
    
    results = client.get(dataset_name, limit=chunk_size, offset=offset, order='collision_id')
    return results

def get_total_record_count(client, dataset_name):
    """
    Retrieve the total record count of a dataset.

    Args:
        client: The client object responsible for interacting with the dataset.
        dataset_name (str): The name of the dataset for which to retrieve the record count.

    Returns:
        int: The total number of records in the dataset.

    Example:
        To get the total record count of a dataset named 'my_dataset', you can call:
        total_count = get_total_record_count(my_client, 'my_dataset')
    """
    
    record_count = client.get(dataset_name, select="COUNT(*)")
    total_records = int(record_count[0]['COUNT'])
    return total_records

def get_api_records(client, api_url, app_token, dataset_name):
    """
    Fetch and aggregate records from an API in parallel using a ThreadPoolExecutor.

    Args:
        client: The client object responsible for interacting with the API.
        api_url (str): The URL of the API endpoint to fetch data from.
        app_token (str): The application token required for authentication (if any).
        dataset_name (str): The name or identifier of the dataset.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the aggregated records from the API.

    Example:
        To fetch and aggregate records from an API endpoint 'https://example.com/api/data',
        with an app token 'my_token', and store them in a DataFrame, you can call:
        df = get_api_records(my_client, 'https://example.com/api/data', 'my_token', 'my_dataset')
    """
    
    chunk_size = 5000
    client.timeout = 100
    
    # Get the total record count
    total_records = get_total_record_count(client, dataset_name)
    
    # Create a ThreadPoolExecutor to fetch data in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        start = 0
        number_of_requests_sent = 0 

        # Fetch data in parallel
        while start < total_records:
            futures.append(executor.submit(fetch_data_chunk, start, chunk_size, client, dataset_name))
            start += chunk_size
            number_of_requests_sent = number_of_requests_sent + 1

        # Collect the results from all futures
        results = []
        for future in concurrent.futures.as_completed(futures):
            chunk = future.result()
            if chunk:
                results.extend(chunk)
    
    print("PARALLEL APPROACH")
    print(f"Total number of records: {total_records}")
    print(f'Number of requests sent {number_of_requests_sent}')
    
    return pd.DataFrame.from_records(results)

def upload_dataframe_to_s3(client, bucket_name, key_name, df, dataset_name):
    """
    Uploads a DataFrame to S3 bucket using the provided AWS S3 client.

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

def main():
    data_url = 'data.cityofnewyork.us'
    socrata_client = Socrata(data_url, app_token)
    crash_data_set = 'h9gi-nx95'
    bucket_name = 'nyc-application-collisions'
    key_name = 'collisions_raw_data'

    # Measure execution time
    start_time = time.time()

    # Call on Threading Method for Mass Download
    crash_df = get_api_records(socrata_client, data_url, app_token, crash_data_set)

    # Connect to AWS boto3 client - Make sure to check the security settings / Add this to the blog entry
    aws_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

    # Upload directly to S3 collisions_raw_data key
    upload_dataframe_to_s3(aws_client, bucket_name, key_name+"/'crash_data_set_par.csv'", crash_df, 'crash_data_set_par.csv')

    # Calculate and print execution time
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds\n")

if __name__ == '__main__':
    main()
