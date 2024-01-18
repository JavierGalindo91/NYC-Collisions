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

## DATA SOURCES and TOOLS
### Data Sources
**NYPD Open Data API**, Powered by Socrata
- Crashes Dataset: [Crashes table](https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95)
- Person Dataset: [Person Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)
- Vehicle Dataset: [Vehicle Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4)

### Tools Used
- **Python 3**: Libraries (pandas, scipy, numpy, boto3, sys, io, sodapy)
- **Docker**: Application for mass upload pipeline.
- **AWS Lambda**: Automating workflows in AWS ecosystem.
- **AWS S3**: Repository for both raw and meticulously processed data.
- **AWS Glue**: Data Processing tool
- **AWS Redshift**: Build the Data Warehouse for OLAP (Online Analytical Processing).
- **Microsoft PowerBI**: Our chosen tool for data visualization.
- **Microsoft PowerPoint**: The canvas for our data story.
  
## Data Pipeline
The following diagram showcases a sophisticated ecosystem, meticulously designed to transform raw data into actionable insights. This data pipeline is the backbone of our project, enabling us to process vast amounts of data efficiently and reliably. Below is an overview of the key components of our data pipeline and the tools employed in each stage:

![Data Pipeline](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/09375b87-113e-4fbf-b496-f87b3e9b411f)

#### Data Collection and Ingestion
_We leverage Python 3 and its powerful libraries such as Pandas, Scipy, Numpy, Boto3, Sys, IO, and Sodapy to build connectors to the NYPD Open Data API. This setup allows us to interface seamlessly with the AWS cloud environment, ensuring a smooth and efficient data ingestion process._

#### Initial Data Processing
_Docker comes into play here, where it is used to create an application for the mass upload pipeline. This approach ensures consistency and scalability in our data processing tasks._

#### Workflow Automation
_AWS Lambda is our tool of choice for automating workflows within the AWS ecosystem. It enables us to manage and automate various processes in the data pipeline, enhancing efficiency and reducing the likelihood of manual errors._

#### Data Storage
_AWS S3 serves as our primary data repository. It hosts both the raw data collected from the API and the processed data, meticulously organized for ease of access and analysis._

#### Data Transformation
_AWS Glue plays a crucial role in our pipeline, extracting raw data from S3 and transforming it into a format suitable for analysis. This transformation includes data cleaning, normalization, and aggregation, preparing the data for in-depth analysis._

#### Data Warehousing for Analysis
_AWS Redshift is used to construct a Data Warehouse for Online Analytical Processing (OLAP). This powerful tool allows us to store and manage large volumes of processed data, making it readily available for complex queries and analysis._

#### Data Visualization and Reporting
_Microsoft PowerBI is our chosen tool for data visualization. It enables us to unearth deep insights from our data and present them in an intuitive, visually compelling format.
For presenting our findings and data narratives, Microsoft PowerPoint serves as our canvas, allowing us to communicate our insights clearly and effectively to stakeholders._
<br>
</br>

The integration of these tools forms a robust and dynamic data pipeline, essential for navigating the complexities of urban driving behavior analysis in the post-pandemic era. It is this pipeline that empowers us to deliver on our promise of data-driven decision-making, adaptability, stakeholder satisfaction, and competitive advantage.

## Accessing Files and Resources
This repository contains all the necessary files and resources used in the NYC Driver Behavior Analysis Project. Here's how to navigate and utilize them:

#### Directory Structure
- **AWS**: Contains scripts and configuration files related to AWS services such as Lambda, S3, and Redshift.
- **Docker**: Includes Dockerfile and related scripts for setting up the Docker containers used in the project.
- **app**: Source code for the main application.
- **data pipelines**: Scripts and code for setting up and managing the data pipelines.
- **data**: This directory is typically used for storing data files. However, due to the sensitive nature of the data, it may not contain raw data files.
- **resources**: Additional resources for the project, such as documentation, configuration files, or reference material.
  - You can access the _**Miro Board**_: via this [link](https://miro.com/app/board/uXjVN9Vu39I=/?share_link_id=875736273394).

## HOW TO USE
To work with the files in this repository, follow these steps:
1. **Clone the Repository**: Clone this repository to your local machine using Git command: `git clone https://github.com/JavierGalindo91/NYC-Collisions.git`
2. **Navigate to Directories**: Use the command line to navigate into any of the directories listed above. For example: `cd NYC-Collisions/AWS`
3. **File Access**: Access files directly within the cloned directories. If you're using an IDE or text editor, you can open the entire project folder to browse through the files.
4. **Running Scripts**: To run scripts, ensure you have the necessary runtime environments set up, such as Python for .py files or Docker for containers. For Python scripts, the command might look like: `python3 script_name.py`
5. **Data Privacy**: Please note that the actual data may be protected due to privacy concerns and thus not available in the repository. If you require access to the data, contact the repository owner at the provided email address.
6. **Updating Files**: If you've made changes and wish to push them to the repository, use the standard Git commands `git add`, `git commit`, and `git push` to update the repository.
7. **Docker Containers**: To work with Docker containers, make sure Docker is installed on your system and use the Docker CLI to build and run containers.
8. **AWS and Cloud Resources**: For AWS resources, you will need appropriate access credentials and permissions. Use the AWS CLI or management console to interact with the services.

### Need Help?
If you encounter any issues or have questions about accessing specific resources, please open an issue in this repository or contact the repository administrator at javier.galindobrito@gmail.com.

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
