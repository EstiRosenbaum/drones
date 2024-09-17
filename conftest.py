import os

import pytest


@pytest.fixture
def delete_log_file():
    os.remove("/usr/share/filebeat/app.log")
    os.removedirs("/usr/share/filebeat/")
