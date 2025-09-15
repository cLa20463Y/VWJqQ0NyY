# 代码生成时间: 2025-09-15 14:55:31
# archive_decompression_tool.py

"""
A simple archive decompression tool using Python and Pyramid framework.
This tool can decompress common archive formats.
"""

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError, HTTPNotFound
import os
import zipfile
import tarfile
# NOTE: 重要实现细节
from io import BytesIO
from pyramid.config import Configurator


# Define a function to handle decompression
# 改进用户体验
def decompress_file(archive_path, output_folder):
    """
    Decompress the archive file to the specified output folder.
    
    :param archive_path: The path to the archive file.
    :param output_folder: The folder where the decompressed files will be placed.
    :return: A tuple with the result message and a boolean indicating success.
    """
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
# NOTE: 重要实现细节
                zip_ref.extractall(output_folder)
            return 'Decompression successful.', True
        elif archive_path.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2')):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(output_folder)
            return 'Decompression successful.', True
# 添加错误处理
        else:
            return 'Unsupported archive format.', False
    except Exception as e:
        return f"An error occurred: {str(e)}", False


# Pyramid view function to handle decompression request
@view_config(route_name='decompress', renderer='json')
# 增强安全性
def decompress_view(request):
    """
    View function to receive a decompression request.
# 改进用户体验
    
    :param request: The Pyramid request object.
# FIXME: 处理边界情况
    :return: A JSON response with the result of the decompression.
# 改进用户体验
    """
    archive_path = request.params.get('archive_path')
    output_folder = request.params.get('output_folder')
    
    if not archive_path or not output_folder:
        return Response({'message': 'Missing archive_path or output_folder parameter.'}, status=400)
# 改进用户体验
    
    # Ensure the archive file exists
    if not os.path.isfile(archive_path):
        return Response({'message': 'Archive file not found.'}, status=404)

    # Ensure the output folder exists
    if not os.path.isdir(output_folder):
        return Response({'message': 'Output folder not found.'}, status=404)

    result, success = decompress_file(archive_path, output_folder)
    if success:
        return Response({'message': result}, status=200)
    else:
# NOTE: 重要实现细节
        return Response({'message': result, 'error': True}, status=500)


# Pyramid main function to configure the application
def main(global_config, **settings):
# 优化算法效率
    """
    Pyramid main function to configure the application.
    
    :param global_config: The global configuration object.
    :param settings: Additional application settings.
# TODO: 优化性能
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('decompress', '/decompress')
    config.scan()
    return config.make_wsgi_app()
