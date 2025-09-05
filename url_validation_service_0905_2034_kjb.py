# 代码生成时间: 2025-09-05 20:34:39
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from urllib.parse import urlparse
import requests

# 定义一个函数来验证URL链接是否有效
def is_valid_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Pyramid视图函数，用于处理URL有效性验证请求
@view_config(route_name='validate_url', renderer='json')
def validate_url(request):
    # 获取URL参数
    url_to_check = request.matchdict['url']
    try:
        # 解析URL确保它是一个有效的URL格式
        parsed_url = urlparse(url_to_check)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return Response(json_body={'message': 'Invalid URL format.'}, status=400)
        
        # 验证URL链接是否有效
        if is_valid_url(url_to_check):
            return Response(json_body={'message': 'URL is valid.', 'status': 'success'}, status=200)
        else:
            return Response(json_body={'message': 'URL is invalid.', 'status': 'error'}, status=400)
    except Exception as e:
        # 错误处理，返回错误信息
        return Response(json_body={'message': 'An error occurred: ' + str(e), 'status': 'error'}, status=500)

# 设置Pyramid配置
def main(global_config, **settings):
    """设置Pyramid应用的配置。"""
    with Configurator(settings=settings) as config:
        # 添加路由
        config.add_route('validate_url', '/validation/{url}')
        # 添加视图
        config.scan()

# 运行Pyramid应用，用于开发和测试
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main(None, {}).make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()