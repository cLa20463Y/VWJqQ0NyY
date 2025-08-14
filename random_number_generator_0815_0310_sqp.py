# 代码生成时间: 2025-08-15 03:10:23
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import random

def random_number_view(request):
    # 获取请求参数
    try:
        min_number = int(request.params.get('min', 0))
        max_number = int(request.params.get('max', 100))
    except ValueError:
        # 处理无效参数，返回错误消息
        return Response("Invalid parameters", status=400)

    # 生成随机数
    random_number = random.randint(min_number, max_number)
    return {'random_number': random_number}

@view_config(route_name='random_number', renderer='json')
def view_random_number(request):
    # 调用随机数生成器视图
    return random_number_view(request)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    with Configurator(settings=settings) as config:
        # 添加随机数生成器路由
        config.add_route('random_number', '/random-number')
        # 添加视图与路由的映射
        config.scan()
    
    return config.make_wsgi_app()
