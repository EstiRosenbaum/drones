import redis
from modules.setup_env import get_env_instance
from server.utils.logger.w_logger import logger


class Redis:
    def __init__(self) -> None:
        try:
            env_value = get_env_instance()
            self.connection = redis.Redis(
                host=env_value.REDIS_HOST,
                port=env_value.REDIS_PORT,
                decode_responses=True,
            )

        except Exception as error:
            logger.error(f"An error occurred while connection to Redis -{error}")

    def update_value_to_folder(
        self, folder_path: str, obj_name: str, value: str
    ) -> None:
        try:
            self.connection.set(f"{folder_path}:{obj_name}", value)
        except Exception as error:
            logger.error(f"Failed to update to {folder_path} in redis - {error}.")

    def remove_value_from_folder(self, folder_path: str, obj_name: str) -> None:
        try:
            self.connection.delete(f"{folder_path}:{obj_name}")
            logger.info(f"Successfully removed from {folder_path} in redis.")
        except Exception as error:
            logger.error(f"Failed to remove from {folder_path} in redis - {error}.")

    def get_keys(self, folder_path: str) -> list:
        try:
            keys = self.connection.keys(f"{folder_path}:*")
            logger.info(f"Successfully get keys from {folder_path} in redis.")
            return keys
        except Exception as error:
            logger.error(f"Failed to get keys from {folder_path} in redis - {error}.")
            return []

    def get_value(self, path: str) -> str:
        try:
            value = self.connection.get(path)
            logger.info(f"Successfully get value from {path} in redis.")
            return value
        except Exception as error:
            logger.error(f"Failed to get value from {path} in redis - {error}.")
