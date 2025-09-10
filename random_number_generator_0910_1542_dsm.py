# 代码生成时间: 2025-09-10 15:42:00
from pyramid.config import Configurator
from pyramid.response import Response
import random
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义一个视图函数，用于生成随机数
def random_number(request):
    # 从请求中获取最小值和最大值参数
    min_val = request.params.get('min', 0)
    max_val = request.params.get('max', 100)
    try:
        # 尝试将参数转换为整数
        min_val = int(min_val)
        max_val = int(max_val)
    except ValueError:
        # 如果参数不是有效的整数，则返回错误信息
        return Response('Invalid integer value for min or max', status=400)
    
    # 生成随机数
    random_num = random.randint(min_val, max_val)
    return Response(f'Random number between {min_val} and {max_val}: {random_num}')

# 配置Pyramid应用
def main(global_config, **settings):
    """
    创建Pyramid应用

    :param global_config: 全局配置对象
    :param settings: 应用设置参数
    :return: 配置好的Pyramid应用
    """
    with Configurator(settings=settings) as config:
        # 添加视图函数
        config.add_route('random_number', '/random')
        config.add_view(random_number, route_name='random_number')
        # 配置扫描当前模块以发现视图函数
        config.scan()

    # 返回配置好的Pyramid应用
    return config.make_wsgi_app()

# 如果直接运行此脚本，则启动Pyramid应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    logger.info('Serving on http://0.0.0.0:6543')
    server.serve_forever()