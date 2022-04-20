from secrets import access_key, secret_access_key
import boto3, os
from botocore.exceptions import ClientError

client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

def upload_my_file(bucket, folder, file_to_upload, file_name):
    key = folder+"/"+file_name
    try:
        response = client.upload_file(file_to_upload, bucket, key)
    except ClientError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
    return True

def upload_to_S3_bucket(bucket_name, key_name, path):
    for top, dirs, files in os.walk(path):
        for file in files:
            individual_file_path = os.path.join(top, file)
            upload_file_bucket = bucket_name
            #upload_file_bucket = 'nyc-application-collisions'
            upload_file_key = key_name + str(file[:-4])
            # upload_file_key = 'collisions/' + str(file[:-4])
            client.put_object(Bucket=upload_file_bucket, Key=(upload_file_key+'/')) #Creating a folder for individual date
            upload_my_file(bucket_name, upload_file_key, individual_file_path, file) # Storing the csv file corresponding to the date in folder

    return 'Successful S3 upload!'
