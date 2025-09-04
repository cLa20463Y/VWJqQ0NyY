# 代码生成时间: 2025-09-05 06:32:42
import os
import shutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# FolderOrganizer class handles the logic for organizing folders
class FolderOrganizer:
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def move_files(self, extension):
        """Move files with given extension from source to target directory."""
        for filename in os.listdir(self.source_dir):
            if filename.endswith(extension):
                src_file = os.path.join(self.source_dir, filename)
                dst_file = os.path.join(self.target_dir, filename)
                try:
                    shutil.move(src_file, dst_file)
                    print(f"Moved: {filename} to {self.target_dir}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")

# Pyramid view function to handle the web request
@view_config(route_name='organize_folders', renderer='json')
def organize_folders(request):
    # Extract parameters from the request
    src_dir = request.params.get('source_dir')
    tgt_dir = request.params.get('target_dir')
    file_ext = request.params.get('file_ext')

    # Validate the directories and file extension
    if not src_dir or not tgt_dir or not file_ext:
        return Response(json_body={'error': 'Missing parameters'}, status=400)

    # Create an instance of FolderOrganizer and move files
    try:
        organizer = FolderOrganizer(src_dir, tgt_dir)
        organizer.move_files(file_ext)
        return Response(json_body={'message': 'Files organized successfully'}, status=200)
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

# Configure the Pyramid application
def main(global_config, **settings):
    """
    Pyramid application setup.

    :param global_config: The global configuration dictionary.
    :param settings: Additional application settings.
    """
    config = Configurator(settings=settings)
    config.add_route('organize_folders', '/organize')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})