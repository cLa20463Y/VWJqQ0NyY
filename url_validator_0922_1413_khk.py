# 代码生成时间: 2025-09-22 14:13:40
from pyramid.config import Configurator
from pyramid.view import view_config
from urllib.parse import urlparse
import requests

def is_valid_url(url):
    """
    验证URL是否有效。
    
    :param url: 待验证的URL字符串。
    :return: 布尔值，True表示URL有效，False表示URL无效。
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fetch_url(url):
    """
    尝试获取URL内容。
    
    :param url: 待获取的URL字符串。
    :return: 布尔值，True表示成功获取内容，False表示获取失败。
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

@view_config(route_name='validate_url', renderer='json')
def validate_url(request):
    """
    验证URL链接有效性的视图函数。
    
    :param request: Pyramid请求对象。
    :return: 包含验证结果的JSON响应。
    """
    url = request.matchdict['url']
    if not is_valid_url(url):
        return {'valid': False, 'message': 'Invalid URL format'}
    if not fetch_url(url):
        return {'valid': False, 'message': 'Failed to fetch URL content'}
    return {'valid': True, 'message': 'URL is valid'}

def main(global_config, **settings):
    """
    Pyramid配置函数。
    
    :param global_config: 全局配置对象。
    :param settings: 额外的设置参数。
    """
    config = Configurator(settings=settings)
    config.add_route('validate_url', '/validate_url/{url}')
    config.scan()
    return config.make_wsgi_app()
