# Setting up the Daily Updates Pipeline on AWS Lambda with Python and Docker

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

Create an IAM role with necessary permissions for Lambda to access other AWS services like ECR. Refer to [permissions_setup.md](AWS/tutorial/permissions_setup.md) for detailed instructions.

## Docker Image Creation

Next, we'll create a Docker image for our application.

### Dockerfile

Ensure you have a Dockerfile in your project directory. You can use the provided Dockerfile as a template.

```Dockerfile
# Your Dockerfile content here


![Daily Updates Pipeline](https://github.com/JavierGalindo91/NYC-Collisions/assets/17058746/3722cbd6-79ac-4a31-b3d0-30320d89ecfb)
