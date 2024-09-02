import unittest
import os

from src.main import add_numbers
from src.main import process_all_donor_files
from src.main import count_files_in_directory

class TestMain(unittest.TestCase):

    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

    def test_count_files_in_principal_dir(self):
        principal_dir = '/Volumes/Backup_6TB/Photos/GooglePhotos/2012'
        self.assertEqual(count_files_in_directory(principal_dir),529)
    
    def test_count_files_in_donor_dir(self):
        donor_dir = '/Users/mike/Desktop/Easter_2024/2012_missing_from_google'
        self.assertEqual(count_files_in_directory(donor_dir),473)

    def test_full_folder_a(self):
        principal_dir = '/Volumes/Backup_6TB/Photos/GooglePhotos/2012'
        donor_dir = '/Users/mike/Desktop/Easter_2024/2012_missing_from_google'
        process_all_donor_files(donor_dir, principal_dir)
        



if __name__ == '__main__':
    unittest.main()