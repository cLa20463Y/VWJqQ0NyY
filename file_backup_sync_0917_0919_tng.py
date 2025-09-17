# 代码生成时间: 2025-09-17 09:19:14
#!/usr/bin/env python

"""
File Backup and Sync Utility

This script is designed to backup and sync files using the Pyramid framework.
It provides a simple and efficient way to manage file synchronization between two directories.

Usage:
  python file_backup_sync.py --source_dir <source_directory> --destination_dir <destination_directory>

Options:
  --source_dir        The directory to backup files from.
  --destination_dir   The directory to sync files to.
  -h --help          Show this screen.

"""

import os
import shutil
import logging
from docopt import docopt
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the backup and sync function
def backup_and_sync(source_dir, destination_dir):
    """
    Backs up and syncs files from source directory to destination directory.
    This function will copy new or updated files from source to destination.
    If a file is deleted from source, it will be deleted from destination as well.
    """
    try:
        # Create the destination directory if it does not exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Get a list of files in both source and destination directories
        src_files = set(os.listdir(source_dir))
        dst_files = set(os.listdir(destination_dir))
        
        # Copy new or updated files from source to destination
        for src_file in src_files:
            if src_file not in dst_files or not os.path.exists(os.path.join(destination_dir, src_file)):
                shutil.copy2(os.path.join(source_dir, src_file), os.path.join(destination_dir, src_file))
                logger.info(f"Copied {src_file} from {source_dir} to {destination_dir}")
            
        # Delete files from destination that are not in source
        for dst_file in dst_files:
            if dst_file not in src_files:
                os.remove(os.path.join(destination_dir, dst_file))
                logger.info(f"Deleted {dst_file} from {destination_dir}")
        
    except Exception as e:
        logger.error(f"Error syncing files: {e}")
        raise

# Define the Pyramid view function
@view_config(route_name='backup_sync', renderer='json')
def backup_sync_view(request):
    """
    View function to handle the backup and sync request.
    It takes the source and destination directories from the request and calls the backup_and_sync function.
    """
    source_dir = request.params.get('source_dir')
    destination_dir = request.params.get('destination_dir')
    if not source_dir or not destination_dir:
        return Response(json_body={'error': 'Source and destination directories are required'}, status=400)
    
    try:
        backup_and_sync(source_dir, destination_dir)
        return Response(json_body={'message': 'Files synchronized successfully'}, status=200)
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

# Define the Pyramid application
def main(global_config, **settings):
    """
    Create a Pyramid WSGI application.
    This function configures the Pyramid application and sets up the routes and views.
    """
    with Configurator(settings=settings) as config:
        config.add_route('backup_sync', '/backup_sync')
        config.scan()
        
    app = config.make_wsgi_app()
    return app

# Run the script if this file is executed directly
if __name__ == '__main__':
    args = docopt(__doc__, version='File Backup and Sync Utility 1.0')
    try:
        backup_and_sync(args['--source_dir'], args['--destination_dir'])
    except Exception as e:
        logger.error(f"Error syncing files: {e}")
        raise