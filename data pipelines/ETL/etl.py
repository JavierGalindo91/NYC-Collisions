import time
import pyarrow
import pandas as pd
import boto3
from io import StringIO, BytesIO

###########################################################################################
################################### Extraction Function ###################################

def extract_csv_from_s3(aws_client, bucket_name, file_name):
    try:
        # Get the object from S3
        response = aws_client.get_object(Bucket=bucket_name, Key=file_name)

        # Read the CSV file content from the response
        csv_content = response['Body'].read()

        # Load the CSV content into a DataFrame
        df = pd.read_csv(BytesIO(csv_content))

        return df

    except Exception as e:
        print(f"Error occurred during extraction: {e}")
        return None

    
###########################################################################################
##################################### Transformations #####################################

def transform_data(dataset, date_column_name, time_column_name):
    """
    Transforms a given dataset by converting date and time columns to datetime objects,
    extracting year, month, day, hour, and minute, and replacing the original date and time columns 
    with a concatenated new column called date_time.

    Args:
    dataset (pandas.DataFrame): The dataset to transform.
    date_column_name (str): The name of the column containing the date information.
    time_column_name (str): The name of the column containing the time information.

    Returns:
    None. The transformation is applied directly to the input DataFrame.
    """
    
    # Convert date column to a pandas datetime object

    dataset[date_column_name] = pd.to_datetime(dataset[date_column_name])

    # Convert time column to pandas datetime object with custom format
    try:
        dataset[time_column_name] = pd.to_datetime(dataset[time_column_name], format='%H:%M')
    except ValueError as e:
        print("Error occurred while parsing time column:")
        for value in dataset[time_column_name]:
            try:
                pd.to_datetime(value, format='%H:%M')
            except ValueError:
                print(f"Invalid value: {value}")

    # Concatenate date and time columns into a new column 'datetime'
    dataset['date_time'] = dataset[date_column_name].dt.strftime('%Y-%m-%dT') + dataset[time_column_name].dt.strftime('%H:%M')

    # Extract year, month, day, hour, and minute from the date and time columns
    dataset['crash_year'] = dataset[date_column_name].dt.year
    dataset['crash_month'] = dataset[date_column_name].dt.month
    dataset['crash_day'] = dataset[date_column_name].dt.day
    dataset['crash_hour'] = dataset[time_column_name].dt.hour
    dataset['crash_minute'] = dataset[time_column_name].dt.minute

    # Drop the original date and time columns
    # dataset.drop([date_column_name, time_column_name], axis=1, inplace=True)
    
    # Reorder columns so the new ones are at the beginning
    new_column_order = [
        'date_time', 'crash_year', 'crash_month', 'crash_day', 'crash_hour', 'crash_minute',
    ] + [col for col in dataset.columns if col not in ['datetime', 'crash_year', 'crash_month', 'crash_day', 'crash_hour', 'crash_minute']]
    
    dataset = dataset[new_column_order]

    print(f'Data has been transformed!')

###############################################################################################
####################################### Upload Functions ######################################

def create_folder(aws_client, bucket_name, prefix):
    aws_client.put_object(Bucket=bucket_name, Key=prefix)

def folder_exists(aws_client, bucket_name, prefix):
    response = aws_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    return 'CommonPrefixes' in response

def create_missing_folders(aws_client, bucket_name, key_name, date_list):
    for date in date_list:
        year = date.year
        month = date.month
        day = date.day
        date_string = f"{year}-{month:02d}-{day:02d}"  # Construct date_string in the desired format
        year_prefix = f"{key_name}/{year}/"
        month_prefix = f"{year_prefix}{month:02d}/"
        day_prefix = f"{month_prefix}{date_string}/"

        # Check if day subfolder exists
        if not folder_exists(aws_client, bucket_name, day_prefix):
            # Day subfolder doesn't exist, create it along with its parent folders
            create_folder(aws_client, bucket_name, year_prefix)
            create_folder(aws_client, bucket_name, month_prefix)
            create_folder(aws_client, bucket_name, day_prefix)


def upload_dataframe_to_s3(aws_client, bucket_name, key_name, DataFrame, date_column_name):
    """
    Uploads a csv DataFrame to S3 bucket, partitioned by date: YYYY-MM-DD.

    Args:
    aws_client: Boto3 client for AWS services.
    bucket_name (str): Name of the S3 bucket.
    key_name (str): Base key name under which data will be stored in S3.
    DataFrame (pandas.DataFrame): DataFrame to upload.
    date_column_name (str): Name of the column containing the date information.

    Returns:
    None
    """

    file_count = 0 

    try:
        # Set the datetime column as the index
        DataFrame[date_column_name] = pd.to_datetime(DataFrame[date_column_name])
        DataFrame.set_index(date_column_name, inplace=True)

        # Group DataFrame by date column
        grouped_data = DataFrame.groupby(pd.Grouper(freq='D'))

        for date, subset_df in grouped_data:
            year = date.year 
            month = date.month 
            day = date.day 
            date_string = f"{year}-{month:02d}-{day:02d}" # Construct date_string in the desired format
            day_subfolder_key = f"{key_name}/{year}/{month:02d}/{date_string}/" # Construct the key path for the day subfolder

            # Check if day subfolder exists
            if not folder_exists(aws_client, bucket_name, day_subfolder_key):
                # Day subfolder doesn't exist, create it along with its parent folders
                create_missing_folders(aws_client, bucket_name, key_name, [date])

            # Save the subset DataFrame as a CSV file in memory
            csv_buffer = StringIO()
            subset_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            # Upload the CSV file to S3 under the day subfolder
            aws_client.put_object(Bucket=bucket_name, Key=f"{day_subfolder_key}{date_string}.csv", Body=csv_buffer.getvalue())

            # Increment the file count
            file_count += 1

    except Exception as e:
        print(f"Error occurred during upload: {e}")
    
    # Print the total number of files uploaded
    print(f"ETL Completed.")
    print(f"Total files uploaded to {key_name} bucket: {file_count}")


#################################################################################################################################

def main():

    ############################### EXTRACT DATA FROM S3 ##########################################
    ###############################################################################################

    start_time = time.time()

    # Set up AWS client and S3 resources
    aws_client = boto3.client(service_name='s3', region_name='us-east-1')
    bucket = 'nyc-application-collisions'
    file_name = "collisions_raw_data/'crash_data_set_par.csv'"

    # Extract CSV file from S3 bucket
    raw_data_df = extract_csv_from_s3(aws_client, bucket, file_name)

    if raw_data_df is not None:
        print("CSV file extracted successfully.")
    else:
        print("Extraction failed.")

    ############################### TRANSFORM DATAFRAME  ##########################################
    ###############################################################################################

    transform_data(raw_data_df, 'crash_date', 'crash_time')

    processed_data_df = raw_data_df

    ############################## UPLOAD PROCESSED DATA  #########################################
    ###############################################################################################

    key_name = 'collisions_processed_data' 
    
    upload_dataframe_to_s3(aws_client, bucket, key_name, processed_data_df, 'date_time')

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Script execution time: {execution_time} seconds")

if __name__ == "__main__":
    main()

