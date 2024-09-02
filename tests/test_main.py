import unittest
import os

from src.main import add_numbers
from src.main import print_exif_data, count_exif_tags
from src.main import file_has_data_time, parse_consistent_date_time_value
from src.main import two_files_have_same_date_time, file_area_in_pixels
from src.main import count_files_in_directory, for_donor_file_what_are_the_prinicpals_to_remove

class TestMain(unittest.TestCase):

    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

    def test_file_exists_00(self):
        # Test that test input file "DSC_0335.jpg" exists
        self.assertTrue(os.path.exists('./tests/inputs/DSC_0335.jpg'))

    def test_file_exists_01(self):
        # Test that test input file "DSC_4397.jpg" exists
        self.assertTrue(os.path.exists('./tests/inputs/DSC_4397.jpg'))

    def test_file00_hasNExifTags(self):
        print_exif_data('./tests/inputs/DSC_0335.jpg')
        n_tags = count_exif_tags('./tests/inputs/DSC_0335.jpg')
        self.assertEqual(n_tags, 12)

    def test_file01_hasNExifTags(self):
        print_exif_data('./tests/inputs/DSC_4397.jpg')
        n_tags = count_exif_tags('./tests/inputs/DSC_4397.jpg')
        self.assertEqual(n_tags, 48)

    def test_both_files_have_data_time(self):
        self.assertTrue(file_has_data_time('./tests/inputs/DSC_0335.jpg'))
        self.assertTrue(file_has_data_time('./tests/inputs/DSC_4397.jpg'))

    def test_can_parse_date_time_00(self):
        value = "2018:12:09 18:56:52"
        isValid, string = parse_consistent_date_time_value(value)
        self.assertTrue(isValid)
        self.assertEqual(string, "2018-12-09 18:56:52")

    def test_can_parse_date_time_01(self):
        hasTag, tagValue = file_has_data_time('./tests/inputs/DSC_0335.jpg')
        self.assertTrue(hasTag)
        isValid, parsedString = parse_consistent_date_time_value(tagValue)
        self.assertTrue(isValid)
        self.assertEqual(parsedString, "2007-05-02 23:37:25")

    def test_can_parse_date_time_02(self):
        hasTag, tagValue = file_has_data_time('./tests/inputs/DSC_4397.jpg')
        self.assertTrue(hasTag)
        isValid, parsedString = parse_consistent_date_time_value(tagValue)
        self.assertTrue(isValid)
        self.assertEqual(parsedString, "2018-12-07 18:51:45")

    def test_compare_files_01(self):
        self.assertFalse(two_files_have_same_date_time('./tests/inputs/DSC_0335.jpg', './tests/inputs/DSC_4397.jpg'))
        self.assertTrue(two_files_have_same_date_time('./tests/inputs/DSC_0335.jpg', './tests/inputs/DSC_0335.jpg'))
        self.assertTrue(two_files_have_same_date_time('./tests/inputs/DSC_4397.jpg', './tests/inputs/DSC_4397.jpg'))

    def test_file_area_00(self):
        self.assertEqual(file_area_in_pixels('./tests/inputs/DSC_0335.jpg'), 2789376)

    def test_count_files_in_principal_dir(self):
        principal_dir = '/Volumes/Backup_6TB/Photos/GooglePhotos/2012'
        self.assertEqual(count_files_in_directory(principal_dir),529)
    
    def test_count_files_in_donor_dir(self):
        donor_dir = '/Users/mike/Desktop/Easter_2024/2012_missing_from_google'
        self.assertEqual(count_files_in_directory(donor_dir),473)

    # For a file in the donor folder
    # Extract the date-time
    # Does this date-time exist in principal_dir?
    # Delete the file(s) from principal_dir
    # Copy in the file from donor dir

    def test_count_files_in_principal_test_dirA(self):
        principal_dir = './tests/inputs/test_principalA'
        self.assertEqual(count_files_in_directory(principal_dir),5)
        donor_dir = './tests/inputs/test_donorA'
        self.assertEqual(count_files_in_directory(donor_dir),2)

    def test_file_area_01(self):
        self.assertEqual(file_area_in_pixels('./tests/inputs/test_donorA/DSC_6315.jpg'), 4983160)

    def test_find_duplicates_6315(self):
        donor = './tests/inputs/test_donorA/DSC_6315.jpg'
        principal_dir = './tests/inputs/test_principalA'
        duplicates = for_donor_file_what_are_the_prinicpals_to_remove(donor,principal_dir)
        self.assertEquals(len(duplicates),2)

    def test_find_duplicates_6352(self):
        donor = './tests/inputs/test_donorA/DSC_6352.jpg'
        principal_dir = './tests/inputs/test_principalA'
        duplicates = for_donor_file_what_are_the_prinicpals_to_remove(donor,principal_dir)
        self.assertEquals(len(duplicates),1)




if __name__ == '__main__':
    unittest.main()