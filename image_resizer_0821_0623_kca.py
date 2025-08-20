# 代码生成时间: 2025-08-21 06:23:34
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from PIL import Image
import os
import logging

log = logging.getLogger(__name__)

# 图片批量处理类
class ImageResizer:
    def __init__(self, directory, output_directory, size):
        self.directory = directory
        self.output_directory = output_directory
        self.size = size

    def resize_images(self):
        """
        遍历目录中的所有图片文件，
        将它们调整至指定尺寸，并保存到输出目录。
        """
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(self.directory, filename)
                output_path = os.path.join(self.output_directory, filename)
                self.resize_image(file_path, output_path)

    def resize_image(self, input_path, output_path):
        """
        调整单个图片文件的尺寸。
        """
        try:
            with Image.open(input_path) as img:
                img = img.resize(self.size, Image.ANTIALIAS)
                img.save(output_path)
                log.info(f'Resized image {input_path} and saved to {output_path}')
        except IOError as e:
            log.error(f'Error resizing image {input_path}: {e}')

# Pyramid视图函数，执行图片尺寸调整
@view_config(route_name='resize_images', renderer='json')
def resize_images(request):
    # 从请求中获取参数
    directory = request.params.get('directory')
    output_directory = request.params.get('output_directory')
    width, height = map(int, request.params.get('size').split('x'))
    size = (width, height)

    # 验证参数
    if not directory or not os.path.isdir(directory):
        return Response(json={'error': 'Invalid directory'}, status=400)
    if not output_directory or not os.path.isdir(output_directory):
        return Response(json={'error': 'Invalid output directory'}, status=400)

    # 创建ImageResizer实例并执行尺寸调整
    resizer = ImageResizer(directory, output_directory, size)
    resizer.resize_images()

    return Response(json={'message': 'Images resized successfully'})

# Pyramid配置函数
def main(global_config, **settings):
    """
    Pyramid WSGI应用程序入口点。
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('resize_images', '/resize')
    config.scan()
    return config.make_wsgi_app()
