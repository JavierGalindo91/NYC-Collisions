# NYC Driver Behavior Analysis Project
## OVERVIEW

I initiated the NYC Driver Behavior Analysis Project with a multifaceted motivation that extends beyond the immediate scenario. While the project addresses the impact of the COVID-19 pandemic on driving behaviors in New York City, it also serves as a platform for personal and professional growth.

### Personal Motivations
**Skill Enhancement**: I aim to polish my data skills and build a comprehensive data portfolio through hands-on experience with real-world datasets.

**End-to-End Learning**: I aspire to gain a holistic understanding of data-driven decision-making processes by immersing myself in every stage of the project lifecycle, including understanding the business context, extracting and processing data from source to delivery, and deriving actionable insights.

**Technology Exploration**: As the owner of this project, I am eager to explore and master the technologies commonly used in similar endeavors, such as leveraging tools like Docker for containerization, AWS Cloud for scalable computing and storage solutions, and database technologies for efficient data management, aiming to expand my technical skill set and adapt to industry-standard practices.

**Domain Expertise**: Delving into the nuances of vehicle collisions in a bustling metropolis like New York City, I seek to broaden my knowledge base and contribute meaningfully to the project's objectives, gaining a deep understanding of this complex issue.
_________________________________________________________________

## SCENARIO: A Brief History of the NYC Driver Behavior

Join us as we delve into the impact of the COVID-19 pandemic on driving behaviors in New York City. Led by The Car Insurance Company TCIC's data and business intelligence team, our mission is clear: 

_**Refine the premium pricing methodology to adapt to significant changes in urban mobility patterns.**_

Our project involves a deep analysis of various datasets to understand how the pandemic has reshaped driving habits, risk factors, and accident trends among our NYC customer base. By leveraging these insights, we aim to make informed decisions within our underwriting and customer service departments, ensuring that our products and services remain relevant to our customers' evolving needs.

The information provided below outlines the business context and expected outcomes for this project. While I'll be sharing some key points from the presentation, you can access the slideshow via the Miro board link provided: [link](https://miro.com/app/board/uXjVN9Vu39I=/?share_link_id=875736273394).

![Business Context](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/6c02fb1e-3ff4-4414-a10b-123e50ef2661)

## METHODOLOGY
In this section, we outline our approach to extracting actionable insights:

![Methodology](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/8915c5a7-7c5c-45b1-9fca-6a95e24696fe)

## DATA SOURCES and TOOLS
### Data Sources
**NYPD Open Data API**, Powered by Socrata
- Crashes Dataset: [Crashes Data](https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95)
- Person Dataset: [Person Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)
- Vehicle Dataset: [Vehicle Data](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4)

### Tools Used
- **Python 3**: Libraries (pandas, scipy, numpy, boto3, sys, io, sodapy)
- **Docker**: Deploy daily updates application through docker container.
- **AWS Lambda**: Automating workflows in AWS ecosystem.
- **AWS S3**: Repository for both raw and meticulously processed data.
- **AWS Glue**: Data Processing tool
- **AWS Redshift**: Build the Data Warehouse for OLAP (Online Analytical Processing).
- **Microsoft PowerBI**: Our chosen tool for data visualization.
- **Miro**: The canvas for our data story.
  
## Data Pipeline
The following diagram showcases a sophisticated ecosystem, meticulously designed to transform raw data into actionable insights. This data pipeline is the backbone of this project, enabling us to process vast amounts of data efficiently and reliably. Below is an overview of the key components of the data pipeline and the tools employed in each stage:

![Data Pipeline](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/696feab4-b588-4870-8e83-6366ca5e4f21)

## Data Ingestion

_**Mass Upload:**_
_To kickstart our data pipeline, I've employed a Python application tailored to directly fetch data from the Socrata API. Once retrieved, this data is securely stored within an S3 bucket dedicated to **raw collisions data**._

_I devised two distinct methods for this upload process: **sequential retrieval** and **parallel retrieval**. Each method has its own set of advantages and drawbacks, extensively discussed within this [tutorial](https://github.com/JavierGalindo91/NYC-Collisions/tree/3552e3bd04fe960cf930641bf296ffe26f109fe8/data%20pipelines/Ingestion%20Pipelines)._

_This initial data influx is executed locally, serving as a crucial step to establish the foundational storage infrastructure, priming the pipeline for subsequent processing stages._
_________________________________________________________________

_**Daily Updates:**_
_A pivotal aspect of this pipeline involves ensuring that our data remains up-to-date with daily advancements. To achieve this, I designed a streamlined pipeline orchestrated to execute daily updates seamlessly._

_Leveraging tools such as Docker containers, AWS ECR (Elastic Container Registry), AWS CloudWatch, AWS Secrets Manager, and AWS Lambda, to automate the ETL (Extract, Transform, Load) process._

_This automated pipeline handles the retrieval and processing of data according to a pre-defined daily schedule, ensuring our dataset remains current and actionable. Please access this [link](https://github.com/JavierGalindo91/NYC-Collisions/tree/3552e3bd04fe960cf930641bf296ffe26f109fe8/AWS) for more details._

## Workflow Automation

_AWS Lambda serves as the backbone for automating workflows within the AWS ecosystem, empowering us to efficiently manage and automate various processes within our data pipeline. By leveraging Lambda, we significantly enhance efficiency while concurrently minimizing the risk of manual errors. This streamlined approach to workflow automation ensures smooth operation throughout the entirety of our data pipeline, facilitating seamless data processing and analysis._

## Data Storage

_AWS S3 serves as the primary data repository, hosting both the raw data collected from the Socrata API and the processed data meticulously organized for ease of access and analysis._

## Data Transformation

_AWS Glue plays a crucial role, extracting raw data from S3 and transforming it into a format suitable for analysis. This transformation includes data cleaning, normalization, and aggregation, preparing the data for in-depth analysis._

## Data Warehousing for Analysis

_AWS Redshift constructs a Data Warehouse for Online Analytical Processing (OLAP). This powerful tool manages large volumes of processed data, making it readily available for complex queries and analysis._

## Data Visualization and Reporting

_Miro is our chosen tool for data visualization. It enables us to unearth deep insights from our data and present them in an intuitive, visually compelling format._
_________________________________________________________________
The integration of these tools forms a robust and dynamic data pipeline, essential for navigating the complexities of urban driving behavior analysis in the post-pandemic era.

## FILE and RESOURCE ACCESS
This repository contains all the necessary files and resources used in the NYC Driver Behavior Analysis Project. Here's how to navigate and utilize them:

#### Directory Structure
- [**AWS**](https://github.com/JavierGalindo91/NYC-Collisions/tree/c6562fe3ff2427a6620679110ca9de2a622db52d/AWS): Contains scripts and configuration files related to AWS services such as Lambda, S3, and Redshift.
- [**Docker**](https://github.com/JavierGalindo91/NYC-Collisions/tree/c6562fe3ff2427a6620679110ca9de2a622db52d/Docker): Includes Dockerfile and related scripts for setting up the Docker containers used in the project.
- [**data pipelines**](https://github.com/JavierGalindo91/NYC-Collisions/tree/main/data%20pipelines): Scripts and code for setting up and managing the data pipelines.
- [**data**](https://github.com/JavierGalindo91/NYC-Collisions/tree/c6562fe3ff2427a6620679110ca9de2a622db52d/data): This directory is typically used for storing data files. However, due to the sensitive nature of the data, it may not contain raw data files.
- [**resources**](https://github.com/JavierGalindo91/NYC-Collisions/tree/c6562fe3ff2427a6620679110ca9de2a622db52d/resources): Additional resources for the project, such as documentation, configuration files, or reference material.

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
I welcome contributions from data analysts, data scientists, and urban mobility experts. If you're interested in contributing to this project, please follow these steps:

1. Fork this repository.
1. Create a new branch for your feature (**git checkout -b feature/YourFeature**).
1. Commit your changes (**git commit -am 'Add some YourFeature'**).
1. Push to the branch (**git push origin feature/YourFeature**).
1. Open a new Pull Request.
1. For any queries or suggestions, feel free to open an issue in the repository.

## Contact Information
For more information on this project please email javier.galindobrito@gmail.com

This README is part of the NYC Driver Behavior Analysis Project initiated by Javier Galindo
