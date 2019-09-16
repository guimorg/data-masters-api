"""Download files from files from AWS Bucket"""
import os
import boto3
import botocore

BUCKET_NAME =  os.getenv('BUCKET_NAME') # replace with your bucket name
KEYS = [file_name for file_name in os.getenv('KEYS').split(';')] # replace with your object key
OUT_DIR = os.getenv('OUT_DIR')

s3 = boto3.resource(
        's3',
        aws_access_key_id=os.getenv('ACCESS_KEY'),
        aws_secret_access_key=os.getenv('SECRET_KEY')
)


def main():
    for key in KEYS:
        try:
            s3.Bucket(BUCKET_NAME).download_file(key, f'{OUT_DIR}/{key}')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise


if __name__ == "__main__":
    main()
