# DATA INGESTION PIPELINES OVERVIEW

You may utilize the following guide as a reference documentation for the Data Ingestion Pipelines developed for this project.

#### OBJECTIVES
The goal of this code is to achieve the following objectives:
- _Retrieve data from the Socrata API endpoint: datasets for collisions, vehicles, and persons in New York City._
-	_Stored the retrieved raw data into pandas DataFrame._
-	_Upload this DataFrame to an AWS S3 bucket called **'nyc-application-collisions/collisions_raw_data/'**_

The diagram below highlights two Data Ingestion processes, as indicated by the milestones within the yellow box:
1. **Mass Upload**: _to be performed once when setting up the application._
2. **Daily Update**: _to be performed in an automated manner via the AWS cloud environment._

![image](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/7a770fd3-dcbe-4297-9765-f9c51ba57a15)

#### DATA SOURCES
The main data source is the NYPD Open Data API, Powered by Socrata:
- Crashes Dataset: [Crashes Data](https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95)
- Person Dataset: [Person Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu/about_data)
- Vehicle Dataset: [Vehicle Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4/about_data)


#### WHERE TO FIND THIS CODE
You can find the scripts for these Data Ingestion Pipelines here:

-	[bruteForce_mass_upload.py](https://github.com/JavierGalindo91/NYC-Collisions/blob/main/data%20pipelines/Ingestion%20Pipelines/bruteForce_mass_upload.py)
- [multiThread_mass_upload.py](https://github.com/JavierGalindo91/NYC-Collisions/blob/main/data%20pipelines/Ingestion%20Pipelines/multiThread_mass_upload.py)
<br></br>

_________________________________________________________________
# MASS UPLOAD DATA INGESTION PIPELINE
As stated in the previous section, we implement a mass upload when setting up the application. We will then deploy this application via Docker in a different tutorial.


We will go over two different methods to download the datasets from the sources above:
-	**Brute Force Method**: _retrieves data from API sequentially._
-	**Multithreading Method**: _uses multithreading to retrieve data in parallel._
_________________________________________________________________
### METHOD #1: BRUTE FORCE

#### **Importing Libraries** 
Import necessary Python libraries and modules: including _time_, _pandas_, _boto3_ for AWS interaction, and _Socrata_ for making requests to the Socrata API.

_This script imports sensitive credentials (app_token, access_key, and secret_access_key) from an external file named secrets_1.py. It is a good practice to keep sensitive information separate from the code._ 

_Please review the documentation below for more information about how to get these credentials:_
 -  https://dev.socrata.com/docs/app-tokens.html
 -  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
_________________________________________________________________
#### How are we fetching records from Socrata API?
The function: _**get_api_records**_ is defined to retrieve records in chunks from the Socrata API and then storing them into a DataFrame.

_**Inputs**_: Socrata client (_client_), API endpoint URL (_api_url_), application token (_app_token_), and dataset name (_dataset_name_).
1.	Initialize some variables like _start, chunk_size_, and set a _timeout_ for the Socrata client. 
2.	Create an empty list, _results_, to store the data from the API responses. 
3.	Calculate the _total number of records_ in the dataset and by doing a total record count.
4.	Fire up requests to the Socrata API until the _start_ counter reaches the _total number of records_.
5.	The data from the API is then retrieved in chunks of 5,000 records until all records are fetched and appended to the _results_ list:
* The Socrata [documentation](https://dev.socrata.com/docs/paging.html#2.1) suggests that our request is ordered by the _collision_id_ field to guarantee that the order of our results will be stable as we page through the dataset.
6.	Finally, return the fetched data as a pandas DataFrame.
_________________________________________________________________
#### How are the records uploaded to S3?
The function: _**upload_dataframe_to_s3**_ is defined to upload a DataFrame to the corresponding AWS S3 bucket.

**_Inputs_**: AWS S3 client (_client_), S3 bucket name (_bucket_name_), object key (_key_name_), the DataFrame (_df_) to be uploaded, and the dataset name (_dataset_name_).
1.	Converts the DataFrame to a CSV format.
2.	Attempt to upload CSV data to the specified S3 bucket and key: _nyc-application-collisions/collisions_raw_data/_:
3.	If the upload is successful, it prints a success message; otherwise, it prints an error message.
_________________________________________________________________
#### Script Execution and Overall Flow
The script checks if it is being executed directly (not imported as a module), and if so, it calls the **_main_** function to initiate the entire process:
1.	Import necessary libraries and credentials.
2.	Define functions for retrieving data from the Socrata API and uploading data to AWS S3.
3.	In the **_main_** function, specify API and S3 details, measure execution time, retrieve data from the Socrata API, upload data to S3, and print execution time.
4.	Run the **_main_** function when the script is executed directly.
_________________________________________________________________
### METHOD #2: MULTITHREADING 

#### **Importing Libraries** 

Import the necessary Python libraries and modules, including _time_, _pandas_, _boto3_ for AWS interaction, _concurrent.futures_ for parallel execution, and _Socrata_ for making requests to the API.

_Just like the Brute Force Method, this script imports sensitive credentials (app_token, access_key, and secret_access_key) from an external file named secrets_1.py. It is a good practice to keep sensitive information separate from the code._

_Please review the documentation below for more information about how to get these credentials:_
 -  https://dev.socrata.com/docs/app-tokens.html
 -  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
_________________________________________________________________
#### How are we fetching records from Socrata API?
_We will define several functions to facilitate different parts of the process._ 
<br></br>

_**Function 1**_: **_fetch_data_chunk_** fetches a chunk of data from a dataset based on the given offset and chunk size.

**_Inputs_**: _offset, chunk size, client object_, and _dataset name_.
- Returns a list of records retrieved from the Socrata API dataset.
 <br> </br>
 
_**Function 2**_: **_get_total_record_count_** retrieves the total record count of a dataset.

**_Inputs_**: _client_ object, and _dataset name_.
- Returns the total number of records in a dataset within the Socrata API.
  <br> </br>

_**Function 3**_: **_get_api_records_** fetches and aggregates records from an API endpoint in parallel using a ThreadPoolExecutor. 

**_Inputs_**: Socrata client (_client_), API endpoint URL (_api_url_), application token (_app_token_), and dataset name (_dataset_name_).
1.	Initialize variable _chunk_size_ and set a _timeout_ for the Socrata client. 
2.	Calculate the _total number of records_ in the dataset by querying the API for the total record count.
3.	Parallel Data Retrieval:     
    - Create multiple threads to fetch data chunks in parallel, improving efficiency.
    - Initialize counter variables _start_, _number of requests_.
    - Create an empty _list_, _futures_, to store results of **concurrent** requests.
    - Send requests to the Socrata API in a loop until the _start_ counter reaches the _total number of records_ in the dataset.
    - A new thread is created for each API request, enabling parallel execution of requests. These threads are stored in the _futures_ list.
4.	Collect and Load Data:
    - Wait for all threads to complete and collect their _results_ into a list.
    - Load the collected data into a DataFrame.
5.	Chunked Retrieval: The data from the API is retrieved in chunks of 5,000 records until all records are fetched and appended to the results list.
6.	Ordering: It's worth noting that we order the API requests by the collision_id field as recommended by Socrata [documentation](https://dev.socrata.com/docs/paging.html#2.1) to ensure the stability of the result order while paging through the dataset.
_________________________________________________________________
#### How are the records uploaded to S3?
We will make use of the same functionality as in the Brute Force Method to upload the data to the AWS S3 bucket.

The function: _**upload_dataframe_to_s3**_ is defined to upload a DataFrame to the corresponding AWS S3 bucket.

**_Inputs_**: AWS S3 client (_client_), S3 bucket name (_bucket_name_), object key (_key_name_), the DataFrame (_df_) to be uploaded, and the dataset name (_dataset_name_).
1.	Converts the DataFrame to a CSV format.
2.	Attempt to upload CSV data to the specified S3 bucket and key: _nyc-application-collisions/collisions_raw_data/_:
3.	If the upload is successful, it prints a success message; otherwise, it prints an error message.
_________________________________________________________________
#### Script Execution and Overall Flow
The **_main_** function serves as the entry point of the script. It is being executed directly (not imported as a module).

Here’s how it works:
1.	It defines API and AWS S3 details, including the API _endpoint URL_, _application token_, dataset name, AWS S3 _bucket name_, and _object key_.
2.	Measures the execution time of the entire process using _time.time()_.
3.	Calls the **_get_api_records_** function to retrieve data from the Socrata API in parallel and stores it in the _crash_df_ DataFrame.
4.	Connects to AWS S3 using the boto3 client.
5.	Calls the **_upload_dataframe_to_s3_** function to upload the retrieved data to the specified S3 bucket.
6.	Calculates and prints the execution time.
_________________________________________________________________
## PERFORMANCE COMPARISON 
To gauge the performance of these methods, we considered the overall Execution Time.

This is done by measuring the total time it takes to retrieve, process, and upload the data to AWS S3. Faster processing time translates to quicker access to up-to-date data.

![image](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/b7b9c969-6f87-4524-af1d-6884d0a199e3)

The Multithreading Method demonstrated significantly improved performance in terms of overall processing time, completing the task in approximately half the time compared to the Brute Force Method.
While both methods successfully retrieved the same dataset of 2M records, the Multithreading Method proved to be more time-efficient in this scenario.

![image](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/7e57dbed-a684-454d-b49b-d4a85d50dadf)
 <br> </br>
_________________________________________________________________
# DAILY UPDATE DATA PIPELINE
Compared to the Mass Upload Data Ingestion Pipelines, the Daily Update Data Pipeline is more comprehensive. It incorporates a complete Extract, Transform, Load (ETL) process to prepare the data for consumption.

This data pipeline is designed to perform the following actions:
- **_Extract_** daily records from the Socrata API.
- **_Transform_** and organize the raw data to match the S3 folder layout.
- **_Load_** the processed dataset to S3 bucket: _**'nyc-application-collisions/collisions_processed_data'**_.

#### **Importing Libraries** 
Import necessary Python libraries and modules: including _time_, _pandas_, _logging_, _io_, _datetime_, _boto3_ for AWS interaction, and _Socrata_ for making requests to the Socrata API.

_This script imports sensitive credentials (app_token, access_key, and secret_access_key) from an external file named secrets_1.py. It is a good practice to keep sensitive information separate from the code._ 

_Please review the documentation below for more information about how to get these credentials:_
 -  https://dev.socrata.com/docs/app-tokens.html
 -  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
_________________________________________________________________
#### Data Extraction
_First, we will set up some tools that will help us interact with the Socrata API. The process employs a straightforward approach for daily data upload, leveraging the Socrata API to retrieve records based on specified criteria with minimal resource consumption._
 <br> </br>

**_Function 1_**: The _**fetch_data_worker**_ function is responsible for retrieving the total count of records from a Socrata dataset within a specified date range.

_**Inputs**_: Socrata client (_socrata_client_), dataset name (_dataset_name_), start date (_starting_date_), current date (_current_date_)

_**Returns**_:	An integer representing the total count of records within the specified date range. If there are no records it returns 0. 
_________________________________________________________________

**_Function 2_**: The _**fetch_data_from_socrata**_ function fetches data from a Socrata dataset starting from a specified date.

_**Inputs**_: Socrata client (_socrata_client_), dataset name (_dataset_name_), start date (_starting_date_)
1. **Initialization**: It sets up parameters such as the chunk size for data retrieval.
2. **Date Formatting**: Formats the start date and current date to be compatible with Socrata API calls.
3. **Fetching Total Records**: Utilizes **_fetch_data_worker_** to determine the total count of records within the specified date range.
4. **Data Retrieval in Chunks**: Iteratively retrieves data from the Socrata API in chunks until all records are fetched.
5. **Data Processing**: Converts the fetched data into a DataFrame.
6. **Output Information**: Prints out relevant information regarding the data extraction process.

_**Returns**_:	A pandas DataFrame containing the fetched data.
_________________________________________________________________
_Now we will set up some tools that will help us interact with the AWS S3 bucket. These functions facilitate the retrieval of temporal information from datasets stored in S3 for further analysis or management._

**_Function 3_**: The _**get_latest_date_in_S3**_ function retrieves the latest date available within a specified dataset stored in an S3 bucket.

_**Inputs**_: AWS client (_aws_client_), S3 Bucket name (_bucket_name_), Key name (_key_name_)

_**Returns**_:	A string representing the latest date available in the dataset.
_________________________________________________________________
**_Function 4_**: The _**get_date_list_in_S3**_ function retrieves a list of unique dates available within a specified location inside an S3 bucket.

_**Inputs**_: AWS client (_aws_client_), S3 Bucket name (_bucket_name_), Key name (_key_name_)
1. **Initialization**: It initializes an empty list to store dates.
2. **List Objects in S3**: It retrieves a list of objects from the specified S3 bucket and key prefix.
3. **Extract Dates**: It parses the object keys to extract dates, assuming a specific key structure.
4. **Date Sorting**: It sorts the extracted dates in descending order to find the latest date or unique dates.
5. **Output**: It returns the latest date or list of unique dates.

_**Returns**_:	A sorted list of unique dates available in the specified location.
_________________________________________________________________
#### Data Transformation
This transformation prepares the dataset for efficient storage and analysis in S3 by standardizing temporal information and optimizing data structure.

**_Function 5_**: The _**transform_data**_ function performs the following transformations on the input Socrata dataset:
- Converts the date and time columns to pandas datetime objects.
- Extracts year, month, day, hour, and minute from the date and time columns.
- Drops the original time column from the dataset.

_**Inputs**_: Dataset extracted from Socrata (_socrata_dataset_), dataset date column name (_date_column_name_), dataset time column name (_time_column_name_)
1. **Date and Time Conversion**: Converts the date and time columns to pandas datetime objects.
2. **Temporal Extraction**: Extracts year, month, day, hour, and minute from the date and time columns.
3. **Column Dropping**: Removes the original time column from the dataset.
   
_**Returns**_:	Nothing. The transformation is applied directly to the input DataFrame.
_________________________________________________________________
#### Data Upload
We will streamline the process of uploading structured data to S3, organizing it by date for efficient storage and retrieval.

**_Function 6_**: The _**upload_dataframe_to_s3**_ function partitions the DataFrame by date and uploads each partition to S3 as a separate CSV file.

_**Inputs**_: AWS clien (_aws_client_), S3 Bucket Name (_bucket_name_), Key name (_key_name_), Transformed dataset (_DataFrame_), dataset date column name (_date_column_name_)
1. **Date Partitioning**: It partitions the DataFrame by unique dates present in the specified date column.
2. **S3 Folder Structure Creation**: It creates a folder structure in S3 according to the year, month, and date.
3. **CSV Conversion**: It converts the DataFrame subset corresponding to each date into a CSV file.
4. **Upload to S3**: It uploads each CSV file to the corresponding date subfolder in S3.
   
_**Returns**_:	Nothing is returned.

- Logging is employed to track the upload process.
- Error handling is implemented to manage exceptions during the upload process.
_________________________________________________________________
#### Script Execution and Overall Flow

The **_main_** function orchestrates the data ingestion process, interacting with both the Socrata API and S3.

Below is a breakdown of its functionality:
1. **Initialization**: It sets up the necessary parameters including the Socrata client, AWS S3 client, bucket name, and key name.
2. **Retrieve Start Date**: It retrieves the latest date available in the S3 bucket to determine the starting point for data extraction from the Socrata API.
3. **Data Extraction**: It fetches data from the Socrata API based on the retrieved start date.
4. **Data Transformation**: It transforms the fetched data to prepare it for uploading to S3.
5. **Upload to S3**: It uploads the transformed data to the specified S3 bucket, partitioned by date.
6. **Execution Time Calculation**: It calculates the execution time of the entire process.

This process ensures efficient data management and analysis by fetching, transforming, and uploading data from the Socrata API to S3 while minimizing redundant data transfer and optimizing resource usage. Additionally, it provides feedback on the readiness of the transformed data for upload and reports the total execution time for monitoring and optimization purposes.
_________________________________________________________________
## PERFORMANCE OVERVIEW
The **_Daily Update Data Pipeline_** demonstrates satisfactory performance in managing data interactions between the Socrata API and S3, specifically within the date range from '_2024-01-01_' to '_2024-02-08_'.

![image](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/f7108ea7-ea73-4768-9088-6db50562583d)

Key performance indicators include:

**Data Retrieval and Transformation**
- The script successfully fetched 8210 records from the Socrata API, demonstrating its capability to handle substantial data volumes effectively.
- Utilizing a "_**Brute Force Approach for Daily Upload**_", the script retrieves all available data without employing sophisticated filtering mechanisms.
- While suitable for daily updates, this method may encounter scalability issues when dealing with notably larger datasets. In such scenarios, considering alternative approaches for data retrieval, such as employing the **_multithread_** method utilized in the _**Mass Upload Data Ingestion pipeline**_, could be beneficial.

**Data Preparation and Upload**
- The fetched data was transformed swiftly, preparing it for upload to S3.
- Transformation activities, such as converting date and time columns and partitioning data by date, were executed seamlessly.
- Each date's data was partitioned and saved as separate CSV files in S3, facilitating efficient data organization and management.

**Execution Time**
- The entire data ingestion process, from retrieval to transformation and upload, was completed within approximately 23.74 seconds. This indicates a reasonable processing time for the volume of data processed and the complexity of the transformation tasks performed.
- While the execution time meets current requirements, ongoing monitoring and optimization efforts may be necessary to ensure continued performance as data volumes grow or processing requirements evolve.
