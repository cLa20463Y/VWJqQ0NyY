# 代码生成时间: 2025-08-14 21:37:02
# decompress_utility.py

"""
A utility for decompressing files using the Pyramid framework.
"""
import os
import zipfile
import tarfile
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError, HTTPBadRequest

# Define a custom exception for unsupported formats
class UnsupportedFormatException(Exception):
    pass

# Define a custom exception for invalid file paths
class InvalidFilePathException(Exception):
    pass

class DecompressUtility:
    """
    A class responsible for handling the decompression of files.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def decompress(self):
        """
        Decompress the file specified by the file path.
        """
        try:
            if self.file_path.endswith('.zip'):
                self._decompress_zip()
            elif self.file_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                self._decompress_tar()
            else:
                raise UnsupportedFormatException('Unsupported file format')
        except zipfile.BadZipFile:
            raise HTTPBadRequest('The file is not a valid zip file.')
        except tarfile.TarError:
            raise HTTPBadRequest('The file is not a valid tar archive.')
        except Exception as e:
            raise HTTPInternalServerError(str(e))

    def _decompress_zip(self):
        """
        Decompress a zip file.
        """
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(self.file_path))

    def _decompress_tar(self):
        """
        Decompress a tar file.
        """
        with tarfile.open(self.file_path, 'r') as tar_ref:
            tar_ref.extractall(os.path.dirname(self.file_path))

@view_config(route_name='decompress', renderer='json')
def decompress_view(request):
    """
    A Pyramid view function to decompress a file.
    """
    file_path = request.params.get('file_path')
    if not file_path:
        return HTTPBadRequest('No file path provided.')
    if not os.path.isfile(file_path):
        return HTTPBadRequest('Invalid file path.')

    try:
        decompressor = DecompressUtility(file_path)
        decompressor.decompress()
        return {'status': 'success', 'message': 'File decompressed successfully.'}
    except (UnsupportedFormatException, InvalidFilePathException, HTTPBadRequest, HTTPInternalServerError) as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return HTTPInternalServerError(str(e))
