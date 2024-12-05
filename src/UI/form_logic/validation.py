import re


def is_valid(control_point, route_path, route_name, include_height=False) -> bool:
    is_control_point_valid = validate_input(control_point)
    is_route_path_valid = validate_route_path_input(route_path, include_height)
    is_route_name_valid = validate_route_name_input(route_name)
    return is_control_point_valid and is_route_path_valid and is_route_name_valid


def validate_input(input_entry) -> bool:
    if is_empty(input_entry.value):
        mark_input_error(input_entry)
        return False
    mark_input_valid(input_entry)
    return True


def validate_route_path_input(route_path, with_height) -> bool:
    if not validate_route_path(route_path.value, with_height):
        mark_input_error(route_path)
        return False
    mark_input_valid(route_path)
    return True


def validate_control_point_input(control_point) -> bool:
    if not validate_control_point(control_point.value):
        mark_input_error(control_point)
        return False
    mark_input_valid(control_point)
    return True


def validate_route_name_input(route_name) -> bool:
    if not validate_route_name(route_name.value):
        mark_input_error(route_name)
        return False
    mark_input_valid(route_name)
    return True


def validate_control_point(cp: str) -> bool:
    num_pattern = r"-?\d*\.?\d+"
    pattern = rf"^{num_pattern},{num_pattern},{num_pattern}$"
    return bool(re.match(pattern, cp))


def validate_route_path(input_str: str, with_height: bool = False) -> bool:
    num_pattern = r"-?\d*\.?\d+"
    pattern = (
        rf"^\s*$|{num_pattern} , {num_pattern}$"
        if not with_height
        else rf"^\s*$|{num_pattern} , {num_pattern} , {num_pattern}$"
    )
    lines = input_str.split("\n")

    if all(line.strip() == "" for line in lines):
        return False

    return all(re.match(pattern, line.strip()) for line in lines)


def validate_route_name(route_name: str) -> bool:
    pattern = r"^[a-zA-Z0-9_\-\.]+$"
    return re.match(pattern, route_name)


def mark_input_error(input, error_text="is not a valid") -> None:
    input.error_text = f"{input.label} {error_text}"


def mark_input_valid(input) -> None:
    input.error_text = None


def is_empty(value: str) -> bool:
    return value == ""
