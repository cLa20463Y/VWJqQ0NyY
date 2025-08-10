# 代码生成时间: 2025-08-10 14:59:15
# unzip_tool.py

"""
A Pyramid application to unzip compressed files.

This application provides a simple interface to unzip files using the Pyramid framework.
It includes basic error handling and follows best practices for Python development.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from zipfile import ZipFile, ZIP_DEFLATED
import os
import io
import mimetypes


# Define a root factory method
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # Add a route for the unzip view
    config.add_route('unzip', '/unzip')
    
    # Add the view for the route
    config.scan()
    return config.make_wsgi_app()

# Define the view for unzipping files
@view_config(route_name='unzip', renderer='json')
def unzip_file(request):
    # Check if the request method is POST
    if request.method != 'POST':
        return Response(json_body={'error': 'This endpoint only supports POST requests.'},
                        content_type='application/json', status=405)

    # Get the uploaded file
    uploaded_file = request.POST['file'].file
    
    # Create a buffer for the file contents
    file_buffer = io.BytesIO(uploaded_file.read())
    
    # Open the zip file in read mode
    with ZipFile(file_buffer, 'r') as zip_ref:
        # Verify the file is a zip file
        if not zip_ref.testzip() is None:
            return Response(json_body={'error': 'The provided file is not a valid zip file.'},
                            content_type='application/json', status=400)
        
        # Unzip the file into a temporary directory
        temp_dir = 'temp_unzip_dir'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        zip_ref.extractall(temp_dir)
        
        # TODO: Implement logic to handle extracted files, e.g., move to a specific directory
        
        # Return a success response
        return Response(json_body={'message': 'File unzipped successfully.'},
                        content_type='application/json', status=200)

# Error handling for unsupported file types
@view_config(context=Exception, renderer='json')
def handle_exception(exc, request):
    return Response(json_body={'error': str(exc)},
                    content_type='application/json', status=500)
