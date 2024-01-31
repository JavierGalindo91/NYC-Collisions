# DATA INGESTION PIPELINES

## OVERVIEW
You may utilize the following guide as a reference documentation for the Data Ingestion Pipelines developed for this project.

#### OBJECTIVES
The goal of this code is to achieve the following objectives:
- _Retrieve data from the Socrata API endpoint: datasets for collisions, vehicles, and persons in New York City._
-	_Stored the retrieved raw data in pandas DataFrames._
-	_Upload this DataFrame to an AWS S3 bucket called **nyc-application-collisions/collisions_raw_data/**_

The diagram below highlights two Data Ingestion processes, as indicated by the milestones within the yellow box:
1. **Mass Upload**: _to be performed once when setting up the application._
2. **Daily Updates**: _to be performed in an automated manner via the AWS cloud environment._

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


## MASS UPLOAD DATA INGESTION PIPELINE
As stated in the previous section, we implement a mass upload when setting up the application. We will then deploy this application via Docker in a different tutorial.

We will go over two different methods to download the datasets from the sources above:
-	**Brute Force Method**: _retrieves data from API sequentially._
-	**Multithreading Method**: _uses multithreading to retrieve data in parallel._

## METHOD #1: BRUTE FORCE
_________________________________________________________________
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
## METHOD #2: MULTITHREADING 
_________________________________________________________________
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
1.	Initialize variable chunk_size and set a timeout for the Socrata client. 
2.	Calculate the total number of records in the dataset by querying the API for the total record count.
3.	Parallel Data Retrieval:     
    - Create multiple threads to fetch data chunks in parallel, improving efficiency.
    - Initialize counter variables start, number of requests.
    - Create an empty list, futures, to store results of concurrent requests.
    - Send requests to the Socrata API in a loop until the start counter reaches the total number of records in the dataset.
    - A new thread is created for each API request, enabling parallel execution of requests. These threads are stored in the futures list.
4.	Collect and Load Data:
    - Wait for all threads to complete and collect their results into a list.
    - Load the collected data into a DataFrame.
5.	Chunked Retrieval: The data from the API is retrieved in chunks of 5,000 records until all records are fetched and appended to the results list.
6.	Ordering: It's worth noting that we order the API requests by the collision_id field as recommended by Socrata [documentation](https://dev.socrata.com/docs/paging.html#2.1) to ensure the stability of the result order while paging through the dataset.
_________________________________________________________________
#### How are the records uploaded to S3?

_________________________________________________________________
#### Script Execution and Overall Flow
