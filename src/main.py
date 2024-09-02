from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil

def print_exif_data(image_path):
    # Open an image file
    image = Image.open(image_path)

    # Extract EXIF data
    exif_data = image._getexif()

    # Print EXIF data
    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag}: {value}")

def count_exif_tags(image_path):
    # Open an image file
    image = Image.open(image_path)

    # Extract EXIF data
    exif_data = image._getexif()

    # Count the number of EXIF tags
    if exif_data:
        return len(exif_data)
    else:
        return 0

def file_has_data_time(image_path):
    # Open an image file
    image = Image.open(image_path)

    # Extract EXIF data
    exif_data = image._getexif()

    # Check if the image has a DateTime tag
    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeDigitized":
                return True, value
    return False

def parse_consistent_date_time_value(value):
    #DateTime: 2018:12:09 18:56:52
    # Parse the value of the DateTime tag
    # 
    try:
        date, time = value.split()
        year, month, day = date.split(":")
        hour, minute, second = time.split(":")
        # format string as "YYYY-MM-DD HH:MM:SS"
        return True, f"{year}-{month}-{day} {hour}:{minute}:{second}"
    except ValueError:
        # Handle the exception if the value cannot be parsed
        print("Invalid DateTime format")
        return False

def two_files_have_same_date_time(file1, file2):
    # Check if two files have the same DateTime tag value
    hasTag1, tagValue1 = file_has_data_time(file1)
    hasTag2, tagValue2 = file_has_data_time(file2)
    if hasTag1 and hasTag2:
        isValid1, parsedString1 = parse_consistent_date_time_value(tagValue1)
        isValid2, parsedString2 = parse_consistent_date_time_value(tagValue2)
        if isValid1 and isValid2:
            return parsedString1 == parsedString2
    return False

def file_area_in_pixels(image_path):
    # Open an image file
    image = Image.open(image_path)

    # Calculate the area of the image
    width, height = image.size
    return width * height

def file_size_in_bytes(image_path):
    # Get the size of an image file in bytes
    return os.path.getsize(image_path)

def split_duplicate_list_keeping_largest(input_list_of_duplicates_files):
    # Return two lists, one of duplicates to remove and one file keep
    # The list of duplicates to remove should be the files with the smallest area in pixels
    # The list of files to keep should be the files with the largest area in pixels
    input_list_of_duplicates_files.sort(key=lambda x: file_area_in_pixels(x))
    return input_list_of_duplicates_files[1:], input_list_of_duplicates_files[:1]

def count_files_in_directory(directory):
    jpg_files = [file for file in os.listdir(directory) if file.lower().endswith('.jpg')]
    # Count the number of .jpg files
    return len(jpg_files)

def for_donor_file_what_are_the_prinicpals_to_remove(donor_file, principal_dir):
    # Get a list of full paths to all .jpg files in the principal_dir
    jpg_files = [
        os.path.join(principal_dir, file) 
        for file in os.listdir(principal_dir) 
        if file.lower().endswith('.jpg')
    ]
    
    # Filter the list based on your condition
    found = [
        file for file in jpg_files 
        if two_files_have_same_date_time(donor_file, file)
    ]

    if len(found) > 0:
        print("Found {} duplicates of {}".format(len(found),donor_file))

    return found

def ensure_subfolder_exists(principal_dir):
    # Ensure that a subfolder named /duplicates exists in the principal_dir
    duplicates_dir = os.path.join(principal_dir, 'duplicates')
    if not os.path.exists(duplicates_dir):
        os.makedirs(duplicates_dir)

def move_duplicates_into_sub_folder(principal_dir,duplicate_file_list):
    # ensure the subfolder /duplicates exists
    ensure_subfolder_exists(principal_dir)
    # move files in duplicate_file_list into the /duplicates subfolder
    duplicates_dir = os.path.join(principal_dir, 'duplicates')
    for file in duplicate_file_list:
        shutil.move(file, duplicates_dir)

def move_donor_into_principal(donor_file, principal_dir):
    # Move the donor_file into the principal_dir
    shutil.move(donor_file, principal_dir)

def process_donor_file(donor_file, principal_dir):
    found = for_donor_file_what_are_the_prinicpals_to_remove(donor_file, principal_dir)
    move_duplicates_into_sub_folder(principal_dir, found)
    move_donor_into_principal(donor_file, principal_dir)

def process_all_donor_files(donor_dir, principal_dir):
    # Get a list of full paths to all .jpg files in the donor_dir
    jpg_files = [
        os.path.join(donor_dir, file) 
        for file in os.listdir(donor_dir) 
        if file.lower().endswith('.jpg')
    ]

    # Process each donor file
    for donor_file in jpg_files:
        process_donor_file(donor_file, principal_dir)


def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b

if __name__ == "__main__":
    result = add_numbers(2, 3)
    print("Result:", result)