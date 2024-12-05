import io

import pandas as pd
from botocore.exceptions import ClientError

from server.s3_api.s3_connection import S3_connection
from server.utils.logger.w_logger import logger

s3_client = S3_connection()


def download_object(bucket_name: str, object_name: str, file_name: str) -> None:
    try:
        s3_client.download_file(bucket_name, object_name, file_name)
        logger.info(f"The file {file_name} was successfully downloaded")
    except Exception as error:
        logger.error(
            f"An error occurred while downloading a file {object_name} -{error}"
        )


def upload_object(bucket_name: str, object_path: str, file_name: str) -> None:
    try:
        s3_client.upload_file(object_path, bucket_name, file_name)
        logger.info(f"The file {file_name} was successfully uploaded")
    except Exception as error:
        logger.error(f"Uploading file failed - {error}")


def create_bucket(bucket_name: str) -> str | None:
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        logger.info(f"The bucket {bucket_name} was successfully created")
    except ClientError as error:
        if error.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            logger.info(f"The bucket {bucket_name} already exists and is owned by you.")
    except Exception as error:
        status_value = (
            f"An error occurred while creating a bucket {bucket_name} -{error}"
        )
        logger.error(status_value)
        return status_value


def get_url(bucket_name: str, object_name: str) -> str | None:
    try:
        url = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket_name, "Key": object_name}
        )
        logger.info("Download generated file")
        return url
    except Exception as error:
        logger.error(f"An error occurred while get url of {object_name} -{error}")


def save_csv_file(data: pd, bucket_name: str, object_name: str):
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, header=False, index=False, encoding="utf-8-sig")
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=csv_buffer.getvalue().encode("utf-8-sig"),
            ContentType="text/csv; charset=utf-8",
        )
        logger.info(f"Successfully uploaded {object_name} to {bucket_name}.")
    except Exception as e:
        logger.error(f"An error occurred while saving the file: {e}.")
