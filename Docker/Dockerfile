# Use the official Python 3.9 image as base
FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY daily_updates_lambda.py ${LAMBDA_TASK_ROOT}

# Install dependencies
COPY requirements.txt /var/task/requirements.txt
RUN pip install --no-cache-dir -r /var/task/requirements.txt

# Set the CMD to your handler
CMD ["daily_updates_lambda.lambda_handler"]
