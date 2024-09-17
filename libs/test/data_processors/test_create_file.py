# import logging
# from logging.handlers import RotatingFileHandler
# from unittest.mock import patch
# from pyfakefs.fake_filesystem_unittest import TestCase
# from unittest.mock import patch, mock_open
# import os
# # import mockfs
# from mockfs import replace_builtins

# # import pytest


# # def create_log_file_for_testing():
# #     os.makedirs("/usr/share/filebeat/")
# #     with open("/usr/share/filebeat/app.log", "w") as file:
# #         file.write("for testing...")
# import pytest
# from pyfakefs.fake_filesystem_unittest import Patcher


# def test_create_directory_with_pyfakefs(fs):
#     # patcher = Patcher()
#     # patcher.setUp()

#     # fake_dir_path = "/usr/share/filebeat/"
#     # patcher.fs.create_dir(fake_dir_path)

#     # assert patcher.fs.exists(fake_dir_path)

    
# # def test_logging_with_mockfs(fs):
#     # Mock the file path
#     # from helpers.logger.w_logger import create_logger
#     log_file_path = '/usr/share/filebeat/app.log'
#     # Create the directory and file in the mocked filesystem
#     fs.create_dir('/usr/share/filebeat/')
#     fs.create_file(log_file_path)
#     assert fs.exists('/usr/share/filebeat/app.log')
#     # Now run the function that writes to the log file
#     # logger = create_logger("test")
#     # logger.info("hello")  # Replace with your log writing function
#     # Read the file to ensure the log entry was written
#     # with open(log_file_path, 'w+') as f:
#     #     f.write("hello")
#     #     log_contents = f.read()
#     # assert "hello" in log_contents
#     # f.close()
#     # patcher.tearDown()

# # @patch('os.makedirs')
# # @patch('builtins.open', new_callable=mock_open)
# # def test_create_log_file_for_testing():
# #     with replace_builtins({"/usr/share/filebeat/app.log":"ddd"}) as mock_os:
# #         with open("/usr/share/filebeat/app.log", "w") as file:
# #             file.write("for testing...")
#     # Assert that os.makedirs was called with the correct path
#     # mock_makedirs.assert_called_once_with("/usr/share/filebeat/")


#     # # Assert that open was called with the correct file path
#     # mock_open.assert_called_once_with("/usr/share/filebeat/app.log", "w")

# class TestCreateLogger(TestCase):
#     def setUp(self):
#         self.setUpPyfakefs()

#     def test_create_logger_with_existing_file(self):
#         self.fs.create_file("/usr/share/filebeat/app.log")
#         with patch('helpers.logger.w_logger.RotatingFileHandler') as mock_handler:
#             from helpers.logger.w_logger import create_logger
#             logger = create_logger(__name__)
#             # mock_handler.assert_called_once_with(
#                 # "/usr/share/filebeat/app.log", maxBytes=10000, backupCount=1)

#             # assert logger.name == __name__
#             # assert logger.level == logging.DEBUG


# if __name__ == '__main__':
#     pytest.main()
