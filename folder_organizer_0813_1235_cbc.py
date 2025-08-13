# 代码生成时间: 2025-08-13 12:35:47
# folder_organizer.py
# This script is a folder organizer that cleans and organizes a directory structure.

import os
import shutil
from datetime import datetime, timedelta
from collections import defaultdict

# Constants for file and folder naming
DOCUMENT_TYPES = {'pdf': 'Documents', 'docx': 'Documents', 'txt': 'Documents'}
IMAGE_TYPES = {'jpg': 'Images', 'jpeg': 'Images', 'png': 'Images'}
AUDIO_VIDEO_TYPES = {'mp3': 'Audios', 'mp4': 'Videos', 'wav': 'Audios'}
ARCHIVE_TYPES = {'zip': 'Archives', 'rar': 'Archives', '7z': 'Archives'}

# Helper functions
def get_extension(file_name):
    """Extracts the file extension from a file name."""
    return file_name.split('.')[-1].lower()

def get_folder_type(file_ext):
    """Determines the folder type based on the file extension."""
    if file_ext in DOCUMENT_TYPES:
        return DOCUMENT_TYPES[file_ext]
    elif file_ext in IMAGE_TYPES:
        return IMAGE_TYPES[file_ext]
    elif file_ext in AUDIO_VIDEO_TYPES:
        if file_ext in AUDIO_VIDEO_TYPES:
            return AUDIO_VIDEO_TYPES[file_ext]
    elif file_ext in ARCHIVE_TYPES:
        return ARCHIVE_TYPES[file_ext]
    else:
        return 'Others'

def organize_folder(source_folder):
    """Organizes the files into their respective folders based on file type."""
    # Create a dictionary to hold the folders and their paths
    folders = defaultdict(list)
    
    # Get the current date to create date-based subfolders
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f'The folder {source_folder} does not exist.')
    
    # Iterate through each file in the source folder
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)
        if os.path.isfile(item_path):
            file_ext = get_extension(item)
            folder_type = get_folder_type(file_ext)
            folder_path = os.path.join(source_folder, folder_type, today)
            
            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            
            # Move the file to the new folder
            shutil.move(item_path, folder_path)
            folders[folder_type].append(item)
        else:
            folders['Folders'].append(item)
    
    return folders

# Main function to run the organizer
def main():
    source_folder = input('Enter the path to the folder you want to organize: ')
    try:
        organized_folders = organize_folder(source_folder)
        print('Folder organization complete.')
        for folder_type, files in organized_folders.items():
            print(f'{folder_type}:
{os.linesep.join(files)}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()