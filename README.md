# NYC Driver Behavior Analysis Project
## OVERVIEW
For this project we will do a mock scenario where we will pretend to be part of a data or business intelligence team at a car insurance company.

### SCENARIO: A Brief History of the NYC Driver Behavior

In this project, we are undertaking an analytical initiative focused on the impact of the COVID-19 pandemic on driving behaviors in New York City. This analysis is conducted by The Car Insurance Company TCIC's data and business intelligence team, with the goal of refining the existing premium pricing methodology in response to the significant changes in urban mobility patterns.

The project involves a deep dive into various datasets to understand how the pandemic has affected driving habits, risk factors, and accident trends among the NYC customer base. Our objective is to utilize these insights to inform decision-making processes within underwriting and customer service, ensuring that our products and services are effectively tailored to meet the current needs of our customers

### Expected Outcomes
- **Data-Driven Decision Making**: Enhancing our underwriting and customer service strategies based on thorough data analysis.
- **Adaptability**: Adjusting our offerings to align with the shifting driving patterns and needs of our customers during and post-pandemic.
- **Stakeholder Satisfaction**: Delivering comprehensive insights to meet and exceed stakeholder expectations.
- **Competitive Advantage**: Using advanced analytics to maintain and strengthen our position in the insurance market.

## METHODOLOGY
### Exploratory Data Analysis
- **Data Discovery**: Scrutinize the data to identify key patterns and anomalies that could influence underwriting decisions.
- **Metadata Analysis**: Gain a deep understanding of our data sources, focusing on accessibility and the structure of the data.

### Deep Dive Analysis
- **Historical Data Examination**: Conduct a thorough analysis of historical data, with a particular emphasis on factors influenced by the pandemic such as risk areas, accident trends, contributing factors, vehicle information, and person-related data.
- **Narrative Building**: Develop a narrative through our analytical approach to make the data speak to both technical and non-technical stakeholders.

## TECHNOLOGY
- **Cloud and Data Management**: Utilize state-of-the-art cloud and data management technologies to facilitate the analysis and seamless communication of insights.
- **Visualization and Reporting Tools**: Employ advanced visualization and reporting tools to unearth deeper findings and present them in an easily digestible format.

## TECHNOLOGY AND DATA SOURCES
### Data Sources: 
**NYPD Open Data API**, Powered by Socrata
- Crashes Dataset: [Crashes table](https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95)
- Person Dataset: [Person Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)
- Vehicle Dataset: [Vehicle Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4)

### Tools Used
- **Python 3**: libraries (pandas, scipy, numpy, boto3, sys, io, sodapy) for building connectors to Open Data API and interfacing with AWS cloud environment.
- **Docker**: Crafting an application for the mass upload pipeline.
- **AWS Lambda**: Automating workflows within the AWS ecosystem.
- **AWS S3**: Repository for both raw and meticulously processed data.
- **AWS Glue**: Extracting raw data and transforming it for the processed storage bucket in S3.
- **AWS Redshift**: Constructing the Data Warehouse for OLAP (Online Analytical Processing).
- **Microsoft PowerBI**: Our chosen tool for data visualization and unearthing insights.
- **PowerPoint**: The canvas for our data story presentation.
  
## HOW TO CONTRIBUTE
We welcome contributions from data analysts, data scientists, and urban mobility experts. If you're interested in contributing to this project, please follow these steps:

1. Fork this repository.
1. Create a new branch for your feature (**git checkout -b feature/YourFeature**).
1. Commit your changes (**git commit -am 'Add some YourFeature'**).
1. Push to the branch (**git push origin feature/YourFeature**).
1. Open a new Pull Request.
1. For any queries or suggestions, feel free to open an issue in the repository.

## Contact Information
For more information on this project please email javier.galindobrito@gmail.com

This README is part of the NYC Driver Behavior Analysis Project initiated by Javier Galindo
