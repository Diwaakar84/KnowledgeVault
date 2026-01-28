import boto3
import uuid
from botocore.config import Config
from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    S3_BUCKET
)

# Initialize the Amazon S3 bucket
s3_config = Config(
    region_name=AWS_REGION,
    signature_version="s3v4",
    s3={"addressing_style": "virtual"}
)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=s3_config
)

# Upload the file to the S3 bucket 
def generate_presigned_upload(file_name: str, file_type: str):
    key = f"uploads/{uuid.uuid4()}-{file_name}"

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": key,
            "ContentType": file_type
        },
        ExpiresIn=3600
    )

    return url, key
