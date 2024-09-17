from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def patch_extracting_time_properties(times_message, current_path):
    return patch(
        f"{current_path}.extracting_time_properties", return_value=times_message
    )


@pytest.fixture
def patch_update_message(class_path):
    return patch(
        f"{class_path}.update_message",
        return_value=Mock(),
    )


@pytest.fixture
def patch_save_message(class_path):
    return patch(
        f"{class_path}.save_message",
        return_value=Mock(),
    )


@pytest.fixture
def patch_calculate_area_per_sortie(current_path):
    return patch(f"{current_path}.get_area_for_sortie", return_value=3)


@pytest.fixture
def exception():
    return pytest.raises(Exception)
