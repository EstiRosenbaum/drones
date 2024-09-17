import os

import pytest

# def create_log_file_for_testing():
#     os.makedirs("/usr/share/filebeat/")
#     with open("/usr/share/filebeat/app.log", "w") as file:
#         file.write("for testing...")


# create_log_file_for_testing()

# def test_create_log_file_for_testing():
#     with replace_builtins({"/usr/share/filebeat/app.log": "ddd"}) as mock_os:
#         with open("/usr/share/filebeat/app.log", "w") as file:
#             file.write("for testing...")

# def test_context():
    # fs = mockfs.replace_builtins()
    # fs.add_entries({'/usr/share/filebeat/app.log':'for testing...'})
    # # mockfs.restore_builtins()
    # # mockfs.MockFS.makedirs(self,path="/usr/share/filebeat/")
    # path = '/usr/share/filebeat'
    # mockfs.mfs.MockFS.makedirs({'/usr/share/filebeat/app.log': 'app'})
    # mockfs.storage.file('/usr/share/filebeat/app.log')
    # mockfs.storage.open('/usr/share/filebeat/app.log', 'w')
    # mockfs.open('/usr/share/filebeat/app.log')
        # mockfs.MockFS.makedirs(path="/usr/share/filebeat")
        # assert os.path.exists('/usr/share/filebeat/app.log')
        # with open('/usr/share/filebeat/app.log', 'r', encoding='utf-8') as fh:
        #     content = fh.read()
        # assert content == 'mockfs'
    # file_content = "for testing..."
    # with patch("os.makedirs", new=()) as mock_dir:
    #     os.makedirs("/usr/share/filebeat")
    #     with patch("builtins.open", mock_open()) as mock_file:
    #         assert open("/usr/share/filebeat/app.log")
    #     mock_file.assert_called_with("/usr/share/filebeat/app.log")
        # os.makedirs("/usr/share/filebeat/")
        
        # with open("/usr/share/filebeat/app.log", "w") as file:
            # file.write(file_content)
    
        # mock_file.assert_called_once_with("/usr/share/filebeat/app.log", "w")
        # mock_file().write.assert_called_once_with(file_content)
# class ExampleTestCase(unittest.TestCase):
#     """The mockfs module can be used in setUp() and tearDown()"""

#     def setUp(self):
#         self.mfs = mockfs.replace_builtins()
#         self.mfs.add_entries({'/usr/share/filebeat': 'test'})
#         self.mfs.storage.open('/usr/share/filebeat/app.log',mode='w')

#     def tearDown(self):
#         mockfs.restore_builtins()

#     def test_using_os_path(self):
#         self.assertEqual(os.listdir('/usr/share'), ['filebeat'])

    # def test_using_open(self):
    #     fh = open('/usr/bin/mockfs-magic')
    #     content = fh.read()
    #     fh.close()
    #     self.assertEqual(data, 'magic')
# def create_eee():
#     with Patcher() as patcher:
#         # access the fake_filesystem object via patcher.fs
#         patcher.fs.create_file("/usr/share/filebeat/app.log", contents="test")

#         # the following code works on the fake filesystem
#         with open("/usr/share/filebeat/app.log") as f:
#             contents = f.read()
# def test_fakefs(fs):
#     fs.create_file('/usr/share/filebeat/app.log')
#     assert os.path.exists('/usr/share/filebeat/app.log')
    
    
# def create_log_file_for_testing():
#     os.makedirs("/usr/share/filebeat/")
#     with open("/usr/share/filebeat/app.log", "w") as file:
#         file.write("for testing...")
    

# class TestCreateLogFileForTesting(unittest.TestCase):
#     # def test_create_log_file_for_testing(self):
#     #     with replace_builtins('os') as mock_os:
#     #         mock_os.makedirs("/usr/share/filebeat/")
#     #         with open("/usr/share/filebeat/app.log", "w") as file:
#     #             file.write("for testing...")
#     @patch('os.makedirs')
#     @patch('builtins.open', new_callable=mock_open)
#     def test_create_log_file_for_testing(self, mock_open, mock_makedirs):
#         create_log_file_for_testing()

#         # Assert that os.makedirs was called with the correct path
#         mock_makedirs.assert_called_once_with("/usr/share/filebeat/")

#         # Assert that open was called with the correct file path
#         mock_open.assert_called_once_with("/usr/share/filebeat/app.log", "w")

# def test_logging_with_mockfs(fs):
#        # Mock the file path
#     from helpers.logger.w_logger import create_logger
#     log_file_path = '/usr/share/filebeat/app.log'
#     # Create the directory and file in the mocked filesystem
#     fs.create_file(log_file_path)
#     # Now run the function that writes to the log file
#     logger=create_logger("test") 
#     logger.info("hello")# Replace with your log writing function
#     # Read the file to ensure the log entry was written
#     with open(log_file_path, 'r') as f:
#         log_contents = f.read()
#         assert "hello" in log_contents

@pytest.fixture
def delete_log_file():
    os.remove("/usr/share/filebeat/app.log")
    os.removedirs("/usr/share/filebeat/")


# if __name__ == '__main__':
#     unittest.main()

# test_context()
# create_eee()
# context_manager()
# # create_log_file_for_testing()
# if __name__ == '__main__':
#     unittest.main()
