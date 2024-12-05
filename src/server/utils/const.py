from enum import Enum


class ConfigFunctionNames(Enum):
    SURFACE = "set_min_distance_from_surface_height"
    RADIUS = "set_location_error_radius"
    RESOLUTION = "set_routing_points_resolution"
    LOS_PLATFORM = "set_safety_distance_below_platform"
    LOS_PEAK = "set_safety_distance_above_peak"
    LOS_ANGLE = "set_safety_angle_from_peak_los"
