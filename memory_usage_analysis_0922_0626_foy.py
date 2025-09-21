# 代码生成时间: 2025-09-22 06:26:59
import os
import psutil
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 定义一个视图函数，用于获取内存使用情况
@view_config(route_name='memory_usage', renderer='json')
def memory_usage(request):
    # 获取当前进程的内存使用信息
    process = psutil.Process(os.getpid())
    try:
        # 使用psutil获取内存使用情况
        memory_info = process.memory_info()
        # 将内存使用量转换为MB
        memory_usage_mb = memory_info.rss / 1024 / 1024
    except Exception as e:
        # 错误处理，返回错误信息
        return {'error': str(e)}
    # 返回内存使用情况的JSON数据
    return {'memory_usage_mb': memory_usage_mb}

# Pyramid应用的配置和启动
def main(global_config, **settings):
    """
    Pyramid WSGI应用程序的入口点。
    """
    config = Configurator(settings=settings)
    config.add_route('memory_usage', '/memory_usage')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()
