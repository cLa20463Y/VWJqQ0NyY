# 代码生成时间: 2025-07-31 04:21:11
# folder_organizer.py

"""
A utility program to organize folders using Pyramid framework.
This program will scan the specified directory,
move files into subdirectories based on file extensions,
and handle potential errors.
"""

import os
import shutil
from pyramid.config import Configurator
from pyramid.response import FileResponse

# Initialize the Pyramid configuration
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('organize', '/organize')
    config.scan()
    return config.make_wsgi_app()

# Function to organize files into subdirectories by extension
def organize_folder(directory):
    """Move files into subdirectories based on their extensions."""
    try:
        # Ensure the directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f"{directory} does not exist.")
        
        # Iterate through all files and directories in the given directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # Check if the item is a file
            if os.path.isfile(item_path):
                file_extension = item.split('.')[-1].lower()
                if file_extension:
                    # Create a subdirectory for the file extension if it doesn't exist
                    subdirectory_path = os.path.join(directory, file_extension)
                    if not os.path.exists(subdirectory_path):
                        os.makedirs(subdirectory_path)
                    # Move the file to the corresponding subdirectory
                    shutil.move(item_path, os.path.join(subdirectory_path, item))
                    print(f"Moved {item} to {subdirectory_path}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

# Pyramid view to handle the organization request
def organize_view(request):
    """View function to organize the folder."""
    directory = request.params.get('directory')
    if not directory:
        return {'error': 'No directory specified.'}
    try:
        organize_folder(directory)
        return {'message': 'Folder organized successfully.'}
    except Exception as e:
        return {'error': str(e)}

# Set up the Pyramid view and route
if __name__ == '__main__':
    # Configure and start the Pyramid application
    from wsgiref.simple_server import make_server
    app = main(None)
    server = make_server('0.0.0.0', 6543, app)
    print('Starting server at http://0.0.0.0:6543/')
    server.serve_forever()