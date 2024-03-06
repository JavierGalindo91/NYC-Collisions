# Setting up the Daily Updates Pipeline on AWS Lambda with Python and Docker

![Daily Updates Pipeline](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/3722cbd6-79ac-4a31-b3d0-30320d89ecfb)

**add diagram to other pipelines!**

## Goals
- Create a Docker image for the Daily Updates application.
- Upload the Docker image to AWS ECR.
- Connect AWS Lambda to the Docker image in ECR for running the application code.

## Prerequisites
- An AWS account with necessary permissions.
- Docker installed on your local machine.
- AWS CLI configured with credentials.

## AWS Housekeeping
The AWS environment must be configured with the correct roles and access permissions.

### Create IAM Roles
Create an IAM role with necessary permissions for Lambda to access other AWS services like ECR and AWS Secrets Manager.

1. Log into the AWS console and navigate to the IAM page.
2. Under Access Management click on Roles.
3. Create new role:
   - Select **AWS service** under the Trusted Entity type.
   - Select **Lambda** for service or use case.
4. Under Add permissions, select the **_AmazonS3FullAccess_** policy and click the **_Next_** button.
5. Enter a Role name.
6. Click on **Create role**.
_________________________________________________________________

### Assign Permissions to the IAM Role
Once the IAM role is created, we can attach permissions policies so the lambda function can freely interact with other AWS services.
1. Under Access Management click on Roles.
2. Select the IAM role we just created.
3. Look for the Add Permissions button and click on the Create inline policy option.
4. Select the appropiate access policies.
   - You may need to create your own inline policies to manage your application's access to specific AWS resources.
   - AWS recommends giving the minimum access required to applications for better management.

Please refer to the AWS [documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) for more information.
_________________________________________________________________

## Creating Docker Application
I created this Python application in a Windows environment. You can follow the steps below;

1. Create new folder on your Desktop.
2. Save the [Dockerfile](https://github.com/JavierGalindo91/NYC-Collisions/blob/7f62e378f8c2ea3d48b8e473b2de5bb52fff573b/Docker/Dockerfile) with the appropiate configuration.
```Dockerfile

# Use the official python 3.9 lambda image from the Amazon ECR Public Gallery
FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY daily_updates_lambda.py ${LAMBDA_TASK_ROOT}

# Install dependencies
COPY requirements.txt /var/task/requirements.txt
RUN pip install --no-cache-dir -r /var/task/requirements.txt

# Set the CMD to your handler
CMD ["daily_updates_lambda.lambda_handler"]
```
I recommend using images from the [Amazon ECR Public Gallery](https://gallery.ecr.aws/lambda/python). These images have been configured to run smoothly in the Lambda Execution environment.
     
4. Save a [requirements.txt](https://github.com/JavierGalindo91/NYC-Collisions/blob/7f62e378f8c2ea3d48b8e473b2de5bb52fff573b/Docker/requirements.txt) file with all the dependencies for your application.
5. Save the python script with the application code.
   - This is where the lambda function lives, so make sure to configure the lambda handler. See the example [here](https://github.com/JavierGalindo91/NYC-Collisions/blob/7f62e378f8c2ea3d48b8e473b2de5bb52fff573b/AWS/daily_updates_lambda.py).
   - I adjusted the code in the [daily updates ingestion pipeline](https://github.com/JavierGalindo91/NYC-Collisions/blob/6543e9745596a489b638dc9343f48a2764d2aa3f/data%20pipelines/Ingestion%20Pipelines/daily_updates.py) so it can be executed inside the Lambda function. Here is a full description of its [functionality](https://github.com/JavierGalindo91/NYC-Collisions/blob/main/data%20pipelines/Ingestion%20Pipelines/ReadME.md#daily-update-data-pipeline). 
_________________________________________________________________
## Building Docker Image and Pushing to AWS ECR

Next, we'll create a Docker image for our application and push it to AWS ECR. Make sure Docker is running and the AWS CLI is installed and configured:

```
# Create ECR Repository if it doesn't exist
aws ecr create-repository --repository-name <repository-name>

# Build docker image
docker build -t <account_id>.dkr.<region>.amazonaws.com/<ECR_repository_name>:<latest version #> .

# Authenticate to registry
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com

# Tag docker image
docker tag <account_id>.dkr.ecr.<region>.amazonaws.com/<ECR_repository_name>:<latest version #> <account_id>.dkr.ecr.<region>.amazonaws.com/<ECR_repository_name>

# Push docker image
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/<ECR_repository_name>
```
_________________________________________________________________
## Deploying Lambda Function from Container Image
Now that the container image is uploaded to the AWS ECR repository, let's create a Lambda function to deploy the application.

