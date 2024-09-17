from typing import Any

import redis
from helpers.logger.w_logger import logger


class Redis:
    def __init__(self) -> None:
        try:
            self.connection = redis.Redis(host="redis", decode_responses=True)
            logger.info("Successfully connected to redis completed.")
        except Exception as error:
            logger.critical(
                f"Failed to initialize variables in the RedisActions class - {error}"
            )

    def remove_obj_from_folder(self, folder_path: str, obj_name: str) -> None:
        try:
            self.connection.json().delete(f"{folder_path}:{obj_name}")
            logger.info(f"Successfully removed {obj_name} from {folder_path} in redis.")
        except Exception as error:
            logger.error(
                f"Failed to remove {obj_name} from {folder_path} in redis - {error}."
            )

    def add_obj_to_folder(self, folder_path: str, obj_name: str, obj: object) -> None:
        try:
            self.connection.json().set(f"{folder_path}:{obj_name}", "$", obj)
            logger.info(f"Successfully added {obj_name} to {folder_path} in redis.")
        except Exception as error:
            logger.error(
                f"Failed to add {obj_name} to {folder_path} in redis - {error}."
            )

    def _get_json(self, path_to_obj: str) -> object:
        return self.connection.json().get(f"{path_to_obj}", "$")[0]

    def update_obj_by_name_and_folder(
        self,
        folder_path: str,
        obj_name: str,
        obj: object = None,
        counter_field_name_to_add: str = None,
    ) -> None:
        try:
            existing_obj = self._get_json(f"{folder_path}:{obj_name}")
            existing_obj = self._update_obj(obj, existing_obj)
            if counter_field_name_to_add is not None:
                existing_obj[counter_field_name_to_add] += 1
            self.add_obj_to_folder(folder_path, obj_name, existing_obj)
            logger.info(
                f"Successfully updated {obj_name} by name and folder {folder_path} in redis."
            )
        except Exception as error:
            logger.error(
                f"Failed to update {obj_name} by name and folder {folder_path} in redis - {error}."
            )

    def _update_obj(self, obj: object, existing_obj: object) -> object:
        if obj:
            for key, value in obj.items():
                existing_obj[key] = value
        return existing_obj

    def delete_folder(self, folder_path: str) -> None:
        try:
            for key in self.connection.keys(f"{folder_path}:*"):
                self.connection.delete(key)
            logger.info(f"Successfully deleted {folder_path} folder from redis.")
        except Exception as error:
            logger.error(f"Failed to delete {folder_path} folder from redis - {error}.")

    def get_field_from_obj_in_folder(
        self, folder_path: str, obj_name: str, field_name: str
    ) -> Any:
        try:
            obj_data = self._get_json(f"{folder_path}:{obj_name}")
            field_value = obj_data.get(field_name)
            logger.info(
                f"Successfully got {field_name} from {obj_name} in {folder_path} in redis."
            )
            return field_value
        except Exception as error:
            logger.error(
                f"Failed to get field {field_name} from {obj_name} in {folder_path} in redis - {error}."
            )

    def get_obj_from_folder(self, folder_path: str, obj_name: str) -> object:
        try:
            object = self._get_json(f"{folder_path}:{obj_name}")
            logger.info(f"Successfully got {obj_name} from {folder_path} in redis.")
            return object
        except Exception as error:
            logger.error(
                f"Failed to get {obj_name} from {folder_path} in redis - {error}."
            )

    def get_folder_content(self, folder_path: str) -> list:
        try:
            folder_keys = self.connection.keys(f"{folder_path}:*")
            json_objs = [self.connection.json().get(key) for key in folder_keys]
            logger.info(f"Successfully got folder content from {folder_path} in redis.")
            return json_objs
        except Exception as error:
            logger.error(
                f"Failed to get folder content from {folder_path} in redis - {error}."
            )

    def obj_exist(self, folder_path: str, obj_name: str) -> bool:
        return self.connection.exists(f"{folder_path}:{obj_name}") != 0
