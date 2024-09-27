import os
import zipfile
import time

# Define source and destination directories
maps_dir = './maps/'
zips_dir = './zips/'

# Create the destination folder if it doesn't exist
if not os.path.exists(zips_dir):
    os.makedirs(zips_dir)

# Function to fix the date and time of the files in the ZIP archive
def add_file_to_zip(zipf, file_path, arcname):
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Create a ZipInfo object to specify the arcname and date/time
    info = zipfile.ZipInfo(arcname)
    # Set the date/time to a fixed value (for example, 2020-01-01 00:00:00)
    info.date_time = (2020, 1, 1, 0, 0, 0)
    # Write the file data to the zip archive with the fixed ZipInfo
    zipf.writestr(info, data)

# Loop over each item in the maps directory
for folder_name in os.listdir(maps_dir):
    folder_path = os.path.join(maps_dir, folder_name)
    
    # Check if it's a directory (folder)
    if os.path.isdir(folder_path):
        # Define the zip file path
        zip_path = os.path.join(zips_dir, f"{folder_name}.zip")
        
        # Create the zip archive
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the folder and add all files
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add the file to the zip archive, preserving the folder structure
                    arcname = os.path.relpath(file_path, maps_dir)
                    add_file_to_zip(zipf, file_path, arcname)
        
        print(f"Zipped: {folder_name}.zip")

print("Zipping completed!")
