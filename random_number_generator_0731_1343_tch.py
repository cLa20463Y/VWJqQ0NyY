# 代码生成时间: 2025-07-31 13:43:40
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import random

def random_number_view(request):
    # 获取请求参数：最小值和最大值
    min_value = request.params.get('min', 1)
    max_value = request.params.get('max', 100)

    try:
        # 将参数转换为整数
        min_value = int(min_value)
        max_value = int(max_value)
    except ValueError:
        # 如果转换失败，返回错误信息
        return Response('Invalid input for min or max. Both should be integers.', status=400)

    # 生成随机数
    random_number = random.randint(min_value, max_value)
    return Response(f'Random number between {min_value} and {max_value}: {random_number}')

# 配置PYRAMID应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 添加视图
    config.add_route('random_number', '/random')
    config.scan()
    return config.make_wsgi_app()

# 如果直接运行，初始化PYRAMID应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    print('Serving on http://0.0.0.0:6543')
    server.serve_forever()