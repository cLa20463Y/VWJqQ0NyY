# 代码生成时间: 2025-09-07 17:33:38
import os
import shutil
from pyramid.config import Configurator
from pyramid.view import view_config

"""
Folder Structure Organizer

This script uses the Pyramid framework to create a web application for organizing folder structures.
It provides a simple interface to move files into subfolders based on their extensions.
"""

class FolderStructureOrganizer:
    """
    A class responsible for organizing folder structures.
    """
    def __init__(self, root_directory):
        self.root_directory = root_directory

    def organize(self):
        """
        Organize files in the root directory into subfolders based on their extensions.
        """
        for root, dirs, files in os.walk(self.root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                extension = self._get_extension(file)
                if not extension:
                    continue

                target_folder = os.path.join(root, extension)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                shutil.move(file_path, target_folder)

    def _get_extension(self, file_name):
        """
        Extract the file extension from a file name.
        """
        return os.path.splitext(file_name)[1].lower()


@view_config(route_name='organize', request_method='GET')
def organize_folder(request):
    "