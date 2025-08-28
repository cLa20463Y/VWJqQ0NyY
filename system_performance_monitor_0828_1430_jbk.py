# 代码生成时间: 2025-08-28 14:30:43
# system_performance_monitor.py

"""
System Performance Monitor using PYRAMID framework.
This application monitors system performance metrics such as CPU usage, memory usage, and disk usage.
"""

from pyramid.config import Configurator
from pyramid.response import Response
import psutil
import json


# Define the root endpoint to return system metrics
# 改进用户体验
def system_metrics(request):
    """
    Return system performance metrics as JSON.
    Includes CPU usage, memory usage, and disk usage.
    """
# 优化算法效率
    try:
# 扩展功能模块
        # Retrieve system metrics
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        # Prepare data to return
        metrics = {
            'CPU Usage': cpu_usage,
            'Memory Usage': {
                'Total': memory.total,
                'Available': memory.available,
# 添加错误处理
                'Used': memory.used,
                'Percentage': memory.percent
# TODO: 优化性能
            },
            'Disk Usage': {
                'Total': disk_usage.total,
                'Used': disk_usage.used,
# NOTE: 重要实现细节
                'Free': disk_usage.free,
                'Percentage': disk_usage.percent
            }
        }

        # Return metrics as JSON
        return Response(json.dumps(metrics), content_type='application/json')
    except Exception as e:
        # Handle errors and return a server error response
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)
# 改进用户体验


# Configure the Pyramid application
def main(global_config, **settings):
    """
    Configure the Pyramid application.
    This function sets up the root endpoint and the necessary settings.
    """
    config = Configurator(settings=settings)
    config.add_route('system_metrics', '/metrics')
    config.add_view(system_metrics, route_name='system_metrics')
    app = config.make_wsgi_app()
    return app


# Run the application if this script is executed directly
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()