# DATA INGESTION PIPELINES

## OVERVIEW
You may utilize the following guide as a reference documentation for the Data Ingestion Pipelines developed for this project.

#### OBJECTIVES
The goal of this code is to achieve the following objectives:
- _Retrieve data from the Socrata API endpoint: datasets for collisions, vehicles, and persons in New York City._
-	_Stored the retrieved raw data in pandas DataFrames._
-	_Upload this DataFrame to an AWS S3 bucket called nyc-application-collisions/collisions_raw_data/_

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
You can find the scripts for these Data Ingestion Pipelines [here](https://github.com/JavierGalindo91/NYC-Collisions/tree/main/data%20pipelines/Ingestion%20Pipelines). 

## MASS UPLOAD DATA INGESTION PIPELINE
As stated in the previous section, we implement a mass upload when setting up the application. We will then deploy this application via Docker in a different tutorial.

We will go over two different methods to download the datasets from the sources above:
-	**Brute Force Method**: _retrieves data from API sequentially._
-	**Multithreading Method**: _uses multithreading to retrieve data in parallel._

#### METHOD #1: BRUTE FORCE

#### **Importing Libraries** 
Import necessary Python libraries and modules: including time, pandas, boto3 for AWS interaction, and Socrata for making requests to the Socrata API.

  _**Please note**_: This script imports sensitive credentials (app_token, access_key, and secret_access_key) from an external file named secrets_1.py. It is a good practice to keep sensitive information separate from the code. 

Please review the documentation below for more information about how to get these credentials:
 -  https://dev.socrata.com/docs/app-tokens.html
 -  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html

 

2.	How are we fetching records from Socrata API?
The function: get_api_records is defined to retrieve records in chunks from the Socrata API and then storing them into a DataFrame. Here's how it works:
Inputs: Socrata client (client), API endpoint URL (api_url), application token (app_token), and dataset name (dataset_name).
1.	Initialize some variables like start, chunk_size, and set a timeout for the Socrata client. 
2.	Create an empty list, results, to store the data from the API responses. 
3.	Calculate the total number of records in the dataset and by doing a total record count.
4.	Fire up requests to the Socrata API until the start counter reaches the total number of records.
5.	The data from the API is then retrieved in chunks of 5,000 records until all records are fetched and appended to the results list:
i.	The Socrata documentation suggests that our request is ordered by the collision_id field to guarantee that the order of our results will be stable as we page through the dataset. [https://dev.socrata.com/docs/paging.html#2.1]
6.	Finally, return the fetched data as a pandas DataFrame.
 

3.	How are the records uploaded to S3?
The function: upload_dataframe_to_s3 is defined to upload a DataFrame to the corresponding AWS S3 bucket. Here's how it works:
Inputs: AWS S3 client (client), S3 bucket name (bucket_name), object key (key_name), the DataFrame (df) to be uploaded, and the dataset name (dataset_name).
1.	Converts the DataFrame to a CSV format.
2.	Attempt to upload CSV data to the specified S3 bucket and key: nyc-application-collisions/collisions_raw_data/:
If the upload is successful, it prints a success message; otherwise, it prints an error message.
 
4.	Script Execution and Overall Flow
The script checks if it is being executed directly (not imported as a module), and if so, it calls the main function to initiate the entire process:
1.	Import necessary libraries and credentials.
2.	Define functions for retrieving data from the Socrata API and uploading data to AWS S3.
3.	In the main function, specify API and S3 details, measure execution time, retrieve data from the Socrata API, upload data to S3, and print execution time.
4.	Run the main function when the script is executed directly.
 
