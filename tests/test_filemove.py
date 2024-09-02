import unittest
import shutil
import os
import tempfile

from src.main import count_files_in_directory, file_size_in_bytes
from src.main import ensure_subfolder_exists, move_duplicates_into_sub_folder
from src.main import process_donor_file, process_all_donor_files

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
    
    def test_can_create_sub_folder(self):
        ensure_subfolder_exists(self.temp_input_folder_principal)
        self.assertTrue(os.path.exists(os.path.join(self.temp_input_folder_principal, 'duplicates')))

    def test_move_all_files_into_sub_folder(self):
        ensure_subfolder_exists(self.temp_input_folder_principal)
        
        # list files in the principal folder
        jpg_files = [
           os.path.join(self.temp_input_folder_principal, file) 
            for file in os.listdir(self.temp_input_folder_principal) 
            if file.lower().endswith('.jpg')
        ]
        self.assertEqual(len(jpg_files),5)
        move_duplicates_into_sub_folder(self.temp_input_folder_principal, jpg_files)
        self.assertEqual(count_files_in_directory(self.temp_input_folder_principal),0)
        self.assertEqual(count_files_in_directory(os.path.join(self.temp_input_folder_principal, 'duplicates')),5)

    def test_full_test_folder_a_DSC_6315(self):
        # The original file size for DSC_6315.jpg in the donor path
        principal_size = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6315.jpg'))
        self.assertEqual(principal_size, 1435944)

        donor_size = file_size_in_bytes(os.path.join(self.temp_input_folder_donor, 'DSC_6315.jpg'))
        self.assertEqual(donor_size, 2368178)

        process_donor_file(os.path.join(self.temp_input_folder_donor, 'DSC_6315.jpg'), self.temp_input_folder_principal)
        # There are two files to remove and replace with 1
        self.assertEqual(count_files_in_directory(self.temp_input_folder_principal), 4)

        principal_size = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6315.jpg'))
        self.assertEqual(principal_size, 2368178)

    def test_full_test_folder_a_DSC_6352(self):
        # The original file size for DSC_6352.jpg in the donor path
        principal_size = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6352.jpg'))
        self.assertEqual(principal_size, 1483802)

        donor_size = file_size_in_bytes(os.path.join(self.temp_input_folder_donor, 'DSC_6352.jpg'))
        self.assertEqual(donor_size, 2199349)

        process_donor_file(os.path.join(self.temp_input_folder_donor, 'DSC_6352.jpg'), self.temp_input_folder_principal)
        # There are 1 files to remove and replace with 1
        self.assertEqual(count_files_in_directory(self.temp_input_folder_principal), 5)

        principal_size = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6352.jpg'))
        self.assertEqual(principal_size, 2199349)

    def test_full_folder_a(self):
        process_all_donor_files(self.temp_input_folder_donor, self.temp_input_folder_principal)
        self.assertEqual(count_files_in_directory(self.temp_input_folder_principal), 4)

        new_size1 = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6315.jpg'))
        self.assertEqual(new_size1, 2368178)
        new_size2 = file_size_in_bytes(os.path.join(self.temp_input_folder_principal, 'DSC_6352.jpg'))
        self.assertEqual(new_size2, 2199349)


if __name__ == '__main__':
    unittest.main()
