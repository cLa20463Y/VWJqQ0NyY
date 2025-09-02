# 代码生成时间: 2025-09-03 05:09:17
import os
import zipfile
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# Constants
FILE_NOT_FOUND_ERROR = 404
INVALID_ARCHIVE_ERROR = 400

class DecompressionService:
    """Service class responsible for handling file decompression."""
    def __init__(self, archive_path):
        self.archive_path = archive_path

    def decompress(self):
        """Decompress the archive to the current directory."""
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as zip_ref:
                zip_ref.extractall()
            return 'Decompression successful.'
        except FileNotFoundError:
            raise Exception('File not found.', FILE_NOT_FOUND_ERROR)
        except zipfile.BadZipFile:
            raise Exception('Invalid archive.', INVALID_ARCHIVE_ERROR)
        except Exception as e:
            raise Exception(f'An error occurred: {str(e)}')

class RootFactory:
    """Root factory for Pyramid application."""
    def __init__(self, request):
        self.request = request

    @view_config(route_name='decompress', renderer='json')
    def decompress_view(self):
        "