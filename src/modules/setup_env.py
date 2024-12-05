import os

from dotenv import load_dotenv

from server.utils.logger.w_logger import logger

load_dotenv()


class _SetupEnv:
    def init_settings(self):
        try:
            self.REDIS_HOST: str = os.environ["REDIS_HOST"]
            self.REDIS_PORT: str = os.environ["REDIS_PORT"]
            self.ENTRYPOINT_URL: str = os.environ["ENTRYPOINT_URL"]
            self.AWS_ACCESS_KEY_ID: str = os.environ["AWS_ACCESS_KEY_ID"]
            self.AWS_SECRET_ACCESS_KEY: str = os.environ["AWS_SECRET_ACCESS_KEY"]
            self.BUCKET_NAME: str = os.environ["BUCKET_NAME"]
            self.LOCK_TIME: str = os.environ["LOCK_TIME"]
            self.DAYS_TO_DELETE_LOG: str = os.environ["DAYS_TO_DELETE_LOG"]

        except KeyError as e:
            logger.error(f"Missing key in env file: {e}")
            raise ValueError(f"Missing key in env file: {e}")
        return self


env = None


def get_env_instance():
    global env
    if env is None:
        env = _SetupEnv().init_settings()
    return env
