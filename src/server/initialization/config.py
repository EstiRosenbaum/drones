import time

import flet as ft

from redis_cache.connect_redis import Redis
from server.config import Config
from server.utils.const import ConfigFunctionNames
from UI.form_logic.helpers import update_status
from UI.utils.const import FolderInRedis


def create_config(
    dict_controls,
    page: ft.Page,
) -> Config:
    try:
        update_status(dict_controls["status"], page, "Working on it...")
        time.sleep(4)
        # Removal after creating a popup
        config = Config(
            dict_controls["route_path"].value,
            dict_controls["type"],
            dict_controls["route_name"].value,
        )
        initialize_value(config, dict_controls["surface"], ConfigFunctionNames.SURFACE)
        initialize_value(config, dict_controls["radius"], ConfigFunctionNames.RADIUS)
        initialize_value(
            config, dict_controls["resolution"], ConfigFunctionNames.RESOLUTION
        )
        initialize_value(
            config, dict_controls["los_platform"], ConfigFunctionNames.LOS_PLATFORM
        )
        initialize_value(
            config, dict_controls["los_peak"], ConfigFunctionNames.LOS_PEAK
        )
        initialize_value(
            config, dict_controls["los_angle"], ConfigFunctionNames.LOS_ANGLE
        )

        redis = Redis()
        control_point = dict_controls["control_point"].value
        value = redis.get_value(f"{FolderInRedis.CONTROL_POINTS}:{control_point}")
        x, y, z = value.split(",")
        config.set_control_point(float(x), float(y), float(z))

        return config
    except Exception:
        return


def initialize_value(config: Config, input, func_name):
    if input.value:
        getattr(config, func_name.value)(int(input.value))
