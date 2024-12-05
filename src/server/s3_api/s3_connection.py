import boto3

from modules.setup_env import get_env_instance
from server.utils.logger.w_logger import logger


def S3_connection():
    try:
        env_value = get_env_instance()
        s3_client = boto3.client(
            "s3",
            endpoint_url=env_value.ENTRYPOINT_URL,
            aws_access_key_id=env_value.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env_value.AWS_SECRET_ACCESS_KEY,
        )
        logger.info("A connection to S3 was successfully established")
        return s3_client
    except Exception as e:
        logger.error(f"An error occurred while try to connect to S3 {e}")
