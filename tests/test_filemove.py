import unittest
import shutil
import os
import tempfile

from src.main import count_files_in_directory

class FileOperationTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Define paths to your original input folders
        self.input_folder_donor = './tests/inputs/test_donorA'
        self.input_folder_principal = './tests/inputs/test_principalA'

        # Define paths to the temporary copies of these folders
        self.temp_input_folder_donor = os.path.join(self.test_dir, 'input_folder_donor')
        self.temp_input_folder_principal = os.path.join(self.test_dir, 'input_folder_principal')

        # Copy the original input folders to the temporary directory
        shutil.copytree(self.input_folder_donor, self.temp_input_folder_donor)
        shutil.copytree(self.input_folder_principal, self.temp_input_folder_principal)

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_file_move_operation(self):
        # Here you would run your code that moves files, using self.temp_input_folder_1 and self.temp_input_folder_2
        self.assertEqual(count_files_in_directory(self.temp_input_folder_donor),2)
        self.assertEqual(count_files_in_directory(self.temp_input_folder_principal),5)
        
        pass  # Replace with actual test code

if __name__ == '__main__':
    unittest.main()
