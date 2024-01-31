# DATA INGESTION PIPELINES

## OVERVIEW
You may utilize the following guide as a reference documentation for the Data Ingestion Pipelines developed for this project.

### OBJECTIVES
The goal of this code is to achieve the following objectives:
- _Retrieve data from the Socrata API endpoint: datasets for collisions, vehicles, and persons in New York City._
-	_Stored the retrieved raw data in pandas DataFrames._
-	_Upload this DataFrame to an AWS S3 bucket called nyc-application-collisions/collisions_raw_data/_

The diagram below highlights two Data Ingestion processes, as indicated by the milestones within the yellow box:
1. **Mass Upload**: _to be performed once when setting up the application._
2. **Daily Updates**: _to be performed in an automated manner via the AWS cloud environment._

![image](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/7a770fd3-dcbe-4297-9765-f9c51ba57a15)
