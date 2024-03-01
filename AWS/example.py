import json
import time
import pyarrow
import pandas as pd
import boto3
from io import StringIO
from sodapy import Socrata
from datetime import datetime

# ------------------------------------------ TOOLS TO INTERACT WITH S3 ------------------------------------------
def get_latest_date_in_S3(aws_client, bucket_name, key_name):
    """
    Get the latest date available in the specified dataset inside S3 bucket.

    Args:
    aws_client: Boto3 client for AWS services.
    dataset_name (str): Name of the dataset.
    bucket_name (str): Name of the S3 bucket.
    key_name (str): Key prefix where the dataset is stored.

    Returns:
    str: The latest date available in the dataset.
    """
    all_dates = []

    # List objects in the base prefix
    response = aws_client.list_objects_v2(Bucket=bucket_name, Prefix=key_name)
    
    # Extract dates from object keys for all years and months
    for obj in response.get('Contents', []):
        key = obj['Key']
        # Split the object key to extract year and month
        parts = key.split('/')
        if len(parts) >= 5: # Assuming a minimum key structure depth
            # Extract date and add to all_dates list
            day = parts[3]
            date_string  = str(datetime.strptime(day, '%Y-%m-%d'))
            all_dates.append(date_string)

    sorted_dates = sorted(all_dates, reverse=True)
    return sorted_dates[0]

def get_date_list_in_S3(aws_client, bucket_name, key_name):
    """
    Get a list of unique dates available in the specified location inside S3 bucket.

    Args:
    aws_client: Boto3 client for AWS services.
    bucket_name (str): Name of the S3 bucket.
    key_name (str): Key prefix where the dataset is stored.

    Returns:
    list: A sorted list of unique dates available in the specified location.
    """
    all_dates =[]

    # List objects in the base prefix
    response = aws_client.list_objects_v2(Bucket=bucket_name, Prefix=key_name)
    
    # Extract dates from object keys for all years and months
    for obj in response.get('Contents', []):
        key = obj['Key']
        # Split the object key to extract year and month
        parts = key.split('/')
        if len(parts) >= 5:
            # Extract year, month and day from the day object and append to the corresponsding lists
            all_dates.append(str(datetime.strptime(parts[3], '%Y-%m-%d')))
           
    sorted_dates = sorted(set(all_dates), reverse=True)
    return sorted_dates

# ------------------------------------------ TOOLS TO EXTRACT DATA FROM SOCRATA API ------------------------------------------
def fetch_data_worker(socrata_client, dataset_name, starting_date, current_date):
    """
    Fetches the total count of records from a Socrata dataset within a specified date range.

    Args:
    socrata_client: Socrata client for interacting with the Socrata API.
    dataset_name (str): Name of the dataset to query.
    starting_date (str): Start date of the date range in 'YYYY-MM-DD' format.
    current_date (str): End date of the date range in 'YYYY-MM-DD' format.

    Returns:
    int: Total count of records within the specified date range. Returns 0 if there are no records or an error occurs.
    """
    count_query = f"SELECT COUNT(*) WHERE crash_date BETWEEN '{starting_date}' AND '{current_date}'"
    response = socrata_client.get(dataset_name, query=count_query)
    
    if response:
        total_records = int(response[0]['COUNT'])
        return total_records
    else:
        return 0

def fetch_data_from_socrata(socrata_client, dataset_name, start_date):
    """
    Fetches data from a Socrata dataset starting from a specified date.

    Args:
    socrata_client: Socrata client for interacting with the Socrata API.
    dataset_name (str): Name of the dataset to fetch data from.
    start_date (str): Start date for fetching data in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
    pandas.DataFrame: DataFrame containing the fetched data.
    """
 
    chunk_size = 3000
    results = []
    start = 0
    number_of_requests_sent = 0
    
    # Rewrite the date strings so we can call the Socrata API -> i.e. '2020-01-01T00:00:00'
    date_format = "%Y-%m-%d %H:%M:%S"
    date_object = datetime.strptime(start_date, date_format)
    starting_date = str(date_object).replace(" ", "T")
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Get the total number of records between the start and current dates
    total_records =  fetch_data_worker(socrata_client, dataset_name, starting_date, current_date)

    # Calling the Socrata API. Extracting data in chunks of 3,000 records
    while True:

        data_chunk  = socrata_client.get(
            dataset_name,
            where=f"crash_date BETWEEN '{starting_date}' AND '{current_date}'",
            offset=start, 
            limit=chunk_size, 
            order='collision_id'
            )
        if not data_chunk:
            # If the current data chunk is empty, we have fetched all available records
            break

        results.extend(data_chunk)
        start += chunk_size
        number_of_requests_sent += 1

    data = pd.DataFrame.from_records(results)
    rec_tot = data.shape[0]

    print()
    print(f"Brute Force Approach for Daily Upload!")
    print(f"Socrata API is returning: {total_records} records")
    print(f'This dataset has {rec_tot} records')
    print(f"Latest record available in S3 is for date: {starting_date}")
    print(f"current date is {current_date}")
    print(f"Number of requests sent: {number_of_requests_sent}")
    print(f"")

    return data

# ------------------------------------------ TRANSFORMING DATA FOR S3 UPLOAD ------------------------------------------
def transform_data(socrata_dataset, date_column_name, time_column_name):
    """
    Transforms the given Socrata dataset by converting date and time columns to datetime objects,
    extracting year, month, day, hour, and minute, and dropping the original time column.

    Args:
    socrata_dataset (pandas.DataFrame): The Socrata dataset to transform.
    date_column_name (str): The name of the column containing the date information.
    time_column_name (str): The name of the column containing the time information.

    Returns:
    None. The transformation is applied directly to the input DataFrame.
    """
    # Convert date column to a pandas datetime object
    socrata_dataset[date_column_name] = pd.to_datetime(socrata_dataset[date_column_name])

    # Convert time column to pandas datetime object with custom format
    try:
        socrata_dataset[time_column_name] = pd.to_datetime(socrata_dataset[time_column_name], format='%H:%M')
    except ValueError as e:
        print("Error occurred while parsing time column:")
        for value in socrata_dataset[time_column_name]:
            try:
                pd.to_datetime(value, format='%H:%M')
            except ValueError:
                print(f"Invalid value: {value}")

    # Extract year, month, day, hour, and minute from the date and time columns
    socrata_dataset['crash_year'] = socrata_dataset[date_column_name].dt.year
    socrata_dataset['crash_month'] = socrata_dataset[date_column_name].dt.month
    socrata_dataset['crash_day'] = socrata_dataset[date_column_name].dt.day
    socrata_dataset['crash_hour'] = socrata_dataset[time_column_name].dt.hour
    socrata_dataset['crash_minute'] = socrata_dataset[time_column_name].dt.minute

    # Drop the original time column
    socrata_dataset.drop([time_column_name], axis=1, inplace=True)

# ------------------------------------------ UPLOADING DATA TO S3 ------------------------------------------
def upload_dataframe_to_s3(aws_client, bucket_name, key_name, DataFrame, date_column_name):
    """
    Uploads a DataFrame to S3 bucket, partitioned by date.

    Args:
    aws_client: Boto3 client for AWS services.
    bucket_name (str): Name of the S3 bucket.
    key_name (str): Base key name under which data will be stored in S3.
    DataFrame (pandas.DataFrame): DataFrame to upload.
    date_column_name (str): Name of the column containing the date information.

    Returns:
    None
    """
    date_list = list(set(DataFrame[date_column_name]))

    for date in date_list:
        try:
            year = date.year 
            month = date.month 
            day = date.day 
            date_string = f"{year}-{month:02d}-{day:02d}" # Construct date_string in the desired format
            day_subfolder_key = f"{key_name}/{year}/{month:02d}/{date_string}/" # Construct the key path for the day subfolder
            
            year_exists = get_date_list_in_S3(aws_client, bucket_name, key_name) # Collect list of available dates in S3

            # Create the year subfolder if it doesn't exist
            if year not in year_exists:
                aws_client.put_object(Bucket=bucket_name, Key=f"{key_name}/{year}/")

                # Check if the month subfolder exists within the year subfolder
                month_exists = get_date_list_in_S3(aws_client, bucket_name, f"{key_name}/{year}/")
                if month not in month_exists:    
                    aws_client.put_object(Bucket=bucket_name, Key=f"{key_name}/{year}/{month:02d}/")

                    # Check if the day subfolder exists within the month subfolder
                    day_exists = get_date_list_in_S3(aws_client, bucket_name, f"{key_name}/{year}/{month:02d}/{date_string}/")
                    if day not in day_exists:
                        aws_client.put_object(Bucket=bucket_name, Key=f"{key_name}/{year}/{month:02d}/{date_string}/")
                    
            # Log the upload process
            #logging.info(f"Uploading file to S3 for: {date_string}")
            print(f'Uploaded file for {date_string}')

            # Filter DataFrame for records corresponding to the current date
            subset_df = DataFrame[DataFrame[date_column_name].dt.date == date.date()]

            # Save the subset DataFrame as a CSV file in memory
            csv_buffer = StringIO()
            subset_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            # Upload the CSV file to S3 under the day subfolder
            aws_client.put_object(Bucket=bucket_name, Key=f"{day_subfolder_key}{date_string}.csv", Body=csv_buffer.getvalue())
        
        except Exception as e:
            print(f"Error occurred while processing date {date}: {e}")

# Initialize Socrata client
def initialize_socrata_client():
    # Set up AWS client for SecretsManager
    secret_name = "custom-managed-secre"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    # Extract app token from SecretsManager
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret_string = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_string)
    app_token = secret_dict['app_token']

    # Set up Socrata client
    data_url = 'data.cityofnewyork.us'
    return Socrata(data_url, app_token)
            
# Lambda handler function
def lambda_handler(event, context):
    # Initialize Socrata client
    socrata_client = initialize_socrata_client()

    # Set up AWS client for S3
    aws_client = boto3.client(service_name='s3', region_name='us-east-1')
    
    # S3 bucket and key 
    bucket_name = 'nyc-application-collisions'
    key_name = 'collisions_processed_data'
    crash_data_set = 'h9gi-nx95'
    
    start_time = time.time()

    # Get the latest date available from S3
    start_date = get_latest_date_in_S3(aws_client, bucket_name, key_name)

    # Make a call to Socrata API using the date range
    api_data = fetch_data_from_socrata(socrata_client, crash_data_set, start_date)

    # Transform api_data prior to uploading to S3
    transform_data(api_data, 'crash_date', 'crash_time')
    print(f"The Socrata data has been transformed!")

    # Upload data to S3
    upload_dataframe_to_s3(aws_client, bucket_name, key_name, api_data, 'crash_date')
    print(f"Daily Upload has been completed!")

    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds\n")

    # Convert Timestamp objects to strings
    api_data['crash_date'] = api_data['crash_date'].astype(str)

    return {
        'statusCode': 200,
        'body': json.dumps(api_data.to_dict(orient='records'))  # Return the DataFrame as JSON
    }

if __name__ == "__main__":
    lambda_handler(None, None)