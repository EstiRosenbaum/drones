from modules.setup_env import get_env_instance
from server.s3_api.s3_actions import create_bucket

bucket_name = get_env_instance().BUCKET_NAME


def create_bucket_s3():
    return create_bucket(bucket_name)
