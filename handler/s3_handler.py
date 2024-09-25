import boto3
import os

from botocore.config import Config
from datetime import datetime

config = Config(region_name='ap-south-1')

s3_client = boto3.client('s3', config=config)


def upload_file(filepath, bucket_name=None, object_name=None):
    uploaded_key = None
    try:
        if not os.path.exists(filepath):
            raise Exception(f"File does not exist at path: {filepath}")

        if not bucket_name:
            raise Exception("bucket_name paramter is required")

        if not object_name:
            object_name = f"{int(datetime.now().timestamp())}.pdf"

        uploaded_file = s3_client.upload_file(filepath, bucket_name, object_name, ExtraArgs={'Metadata': {'Content-Type': 'application/pdf'}})
        print(uploaded_file)
    except Exception as e:
        print(f"Error in upload_file: {filepath}:", e)

    return uploaded_key
