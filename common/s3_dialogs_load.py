import os
import boto3
import botocore.session


def load_from_s3(aws_session: boto3.Session, s3_bucket: str, s3_folder: str, local_folder: str):
    s3 = aws_session.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=s3_bucket, Prefix=s3_folder)
    os.makedirs(os.path.dirname(local_folder), exist_ok=True)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                s3_key = obj['Key']
                if s3_key.endswith("/") or not s3_key.lower().endswith(".json"):
                    continue
                # Construct local file path, preserving folder structure
                relative_path = os.path.relpath(
                    s3_key, s3_folder).replace(" ", "_")
                local_file_path = os.path.join(local_folder, relative_path)

                try:
                    print(f"Downloading {s3_key} to {local_file_path}...")
                    s3.download_file(s3_bucket, s3_key, local_file_path)
                except Exception as e:
                    print(f"Error downloading {s3_key}: {e}")
