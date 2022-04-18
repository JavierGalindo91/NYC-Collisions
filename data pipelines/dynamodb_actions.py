from secrets import access_key, secret_access_key
from pandas.core.dtypes.missing import notnull
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import boto3, pandas as pd


s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_access_key
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key,
    )

# Load csv file directly into python
obj = s3.Bucket('nyc-application-collisions').Object('collisions/collisions.csv').get()
csv_file = pd.read_csv(obj['Body'])

class Collision(BaseModel):
    collision_id: str
    crash_date: Optional[str]
    crash_time: Optional[str]
    Boroughs: Optional[str]
    zip_code: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    number_of_persons_injured: Optional[int]
    number_of_persons_killed: Optional[int]
    number_of_pedestrians_injured: Optional[int]
    number_of_pedestrians_killed: Optional[int]
    number_of_cyclist_injured: Optional[int]
    number_of_cyclist_killed: Optional[int]
    number_of_motorist_injured: Optional[int]
    number_of_motorist_killed: Optional[int]
    contributing_factor_vehicle_1: Optional[str]
    contributing_factor_vehicle_2: Optional[str]
    vehicle_type_code1: Optional[str]
    vehicle_type_code2: Optional[str]

# Parse each json blob from list
def create_crash(sentCollision: Collision):
    sentCollision = sentCollision.to_dict(orient = 'records')
    return sentCollision

json_sample = create_crash(csv_file)

def save_to_dynamodb(json_blob,dynamodb_table_name):

    return dynamodb.Table(dynamodb_table_name).put_item(
    Item={
        'collision_id': str(json_blob['collision_id']),
        'zip_code': str(json_blob['zip_code']),
        'crash_date': json_blob['crash_date'],
        'crash_time': json_blob['crash_time'],
        'Boroughs': json_blob['Boroughs'],
        'latitude': json_blob['latitude'],
        'longitude': json_blob['longitude'],
        'number_of_persons_injured': Decimal(json_blob['number_of_persons_injured']),
        'number_of_persons_killed': Decimal(json_blob['number_of_persons_killed']),
        'number_of_pedestrians_injured': Decimal(json_blob['number_of_pedestrians_injured']),
        'number_of_pedestrians_killed': Decimal(json_blob['number_of_pedestrians_killed']),
        'number_of_cyclist_injured': Decimal(json_blob['number_of_cyclist_injured']),
        'number_of_cyclist_killed': Decimal(json_blob['number_of_cyclist_killed']),
        'number_of_motorist_injured': Decimal(json_blob['number_of_motorist_injured']),
        'number_of_motorist_killed': Decimal(json_blob['number_of_motorist_killed']),
        'contributing_factor_vehicle_1': str(json_blob['contributing_factor_vehicle_1']),
        'contributing_factor_vehicle_2': str(json_blob['contributing_factor_vehicle_2']),
        'vehicle_type_code1': json_blob['vehicle_type_code1'],
        'vehicle_type_code2': json_blob['vehicle_type_code2'],
        }
    )

for i in range(0, 15):
    save_to_dynamodb(json_sample[i],'nyc-collisions-table')