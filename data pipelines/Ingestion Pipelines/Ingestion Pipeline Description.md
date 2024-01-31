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
As stated in the previous season, a mass upload is done when setting up the application. We will then deploy this application via Docker in a different tutorial.

We will go over two different methods to download the datasets from the sources above:
-	**Brute Force Method**: _retrieves data from API sequentially._
-	**Multithreading Method**: _uses multithreading to retrieve data in parallel._

#### METHOD #1: BRUTE FORCE
