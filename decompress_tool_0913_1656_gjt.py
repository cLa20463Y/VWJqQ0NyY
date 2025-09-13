# 代码生成时间: 2025-09-13 16:56:32
# decompress_tool.py

"""
A Pyramid application that serves as a file decompression tool.
This script uses the `zipfile` module to handle zip file decompression.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from zipfile import ZipFile, is_zipfile
import os
import mimetypes
import logging

# Set up logger
log = logging.getLogger(__name__)


@view_config(route_name='decompress', renderer='json')
def decompress_view(request):
    # Get the uploaded file from the request
    input_file = request.POST['file'].file
    filename = input_file.filename
    
    # Check if the file is a zip file
    if not is_zipfile(input_file):
        return {'error': 'The uploaded file is not a zip file.'}
    
    # Define the directory to store the extracted files
    extract_dir = os.path.join('extracted', filename)
    try:
        # Create the directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)
        
        # Open the zip file and extract its contents
        with ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Return a success message with the number of files extracted
        num_files = len([name for name in os.listdir(extract_dir) if os.path.isfile(os.path.join(extract_dir, name))])
        return {'message': f'Files extracted successfully. Total files: {num_files}.'}
    except Exception as e:
        # Handle any exceptions that occur during extraction
        log.error(f'An error occurred during extraction: {e}')
        return {'error': 'An error occurred during file extraction.'}

# Configure the Pyramid app with the decompression view
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('decompress', '/decompress')
    config.scan()
    return config.make_wsgi_app()
