# 代码生成时间: 2025-09-03 14:16:56
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from PIL import Image
from io import BytesIO

# 图片尺寸批量调整器视图类
class ImageResizer:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='image_resize', renderer='json')
    def image_resize_view(self):
        """
        处理图片尺寸批量调整请求的视图函数
        """
        try:
            image_path = self.request.params.get('image_path')
            target_size = self.request.params.get('target_size')
            output_path = self.request.params.get('output_path')

            if not image_path or not target_size or not output_path:
                return {'error': 'Missing parameters'}

            target_size = tuple(map(int, target_size.split(',')))
            self.resize_images(image_path, target_size, output_path)

            return {'message': 'Images resized successfully'}
        except Exception as e:
            return {'error': str(e)}

    def resize_images(self, image_path, target_size, output_path):
        """
        批量调整图片尺寸
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'The image path {image_path} does not exist.')

        for filename in os.listdir(image_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(image_path, filename)
                self.resize_image(file_path, target_size, output_path)

    def resize_image(self, image_path, target_size, output_path):
        """
        调整单个图片尺寸
        """
        try:
            with Image.open(image_path) as img:
                img = img.resize(target_size)
                output_file_path = os.path.join(output_path, os.path.basename(image_path))
                img.save(output_file_path)
        except Exception as e:
            raise Exception(f'Failed to resize image {image_path}: {str(e)}')

# 初始化和配置Pyramid应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('image_resizer')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main()
