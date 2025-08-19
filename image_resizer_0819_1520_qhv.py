# 代码生成时间: 2025-08-19 15:20:44
import os
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from PIL import Image

# 图片尺寸批量调整器配置
class ImageResizerConfigurator(Configurator):
    def __init__(self, settings):
        super().__init__(settings=settings)
        self.add_route('resize_images', '/resize')

# 图片尺寸批量调整器视图
class ImageResizer:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='resize_images', renderer='json')
    def resize_images(self):
        # 获取请求参数
        target_directory = self.request.params.get('target_directory')
        new_width = int(self.request.params.get('new_width', 0))
        new_height = int(self.request.params.get('new_height', 0))

        # 参数校验
        if not target_directory or new_width <= 0 or new_height <= 0:
            return {'error': 'Invalid parameters'}

        try:
            # 遍历目标目录中的所有文件
            for filename in os.listdir(target_directory):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    file_path = os.path.join(target_directory, filename)
                    # 打开图片文件
                    with Image.open(file_path) as img:
                        # 调整图片尺寸
                        resized_img = img.resize((new_width, new_height))
                        # 保存调整后的图片
                        resized_img.save(file_path)

            # 返回成功响应
            return {'message': 'Images resized successfully'}
        except Exception as e:
            # 错误处理
            return {'error': str(e)}

# Pyramid应用配置和初始化
def main(global_config, **settings):
    config = ImageResizerConfigurator(settings)
    config.scan()
    app = config.make_wsgi_app()
    return app

# 如果直接运行脚本，则启动应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('', 8080, main) as server:
        print('Serving on http://127.0.0.1:8080/')
        server.serve_forever()