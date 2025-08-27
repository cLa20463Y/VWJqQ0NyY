# 代码生成时间: 2025-08-27 08:06:50
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import requests
from urllib.parse import urlparse

# 定义一个简单的URL验证器，用于检查给定的URL是否有效并可访问。
class URLValidator:
    def __init__(self, request):
        self.request = request

    # 验证URL是否有效
    def validate_url(self, url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            # 如果HTTP响应状态码为200，则URL有效
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            # 请求异常，如超时或连接错误
            return False

# Pyramid视图函数
@view_config(route_name='validate_url', renderer='json')
def validate_url_view(request):
    # 从请求中获取URL参数
    url = request.params.get('url')
    if not url:
        # 没有提供URL参数，返回错误响应
        return Response('{"error": "Missing URL parameter"}', content_type='application/json')

    url_validator = URLValidator(request)
    is_valid = url_validator.validate_url(url)

    # 返回JSON格式的响应，包含URL验证结果
    response_body = {"url": url, "is_valid": is_valid}
    return Response(json.dumps(response_body), content_type='application/json')

# 初始化Pyramid配置器
def main(global_config, **settings):
    config = Configurator(settings=settings)
    # 添加路由
    config.add_route('validate_url', '/validate')
    # 添加视图
    config.scan()
    return config.make_wsgi_app()
