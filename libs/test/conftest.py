import os
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_env():
    return patch.dict(
        os.environ, {"NAME": "user", "CLOUD_ID": "cloud_id", "PASSWORD": "pass"}
    )


@pytest.fixture
def exception():
    return pytest.raises(Exception)
