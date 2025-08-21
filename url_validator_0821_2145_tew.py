# 代码生成时间: 2025-08-21 21:45:22
from urllib.parse import urlparse
# TODO: 优化性能
from pyramid.view import view_config
# 扩展功能模块
from pyramid.response import Response
import requests

def is_valid_url(url):
    # 验证URL格式是否正确
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
# 增强安全性

def validate_url(context, request):
# 扩展功能模块
    # 获取URL参数
    input_url = request.params.get('t')
    
    # 检查URL是否为空
    if not input_url:
        return Response("URL parameter 't' is missing", status=400)
    
    # 检查URL是否有效
    if not is_valid_url(input_url):
        return Response("Invalid URL format", status=400)
    
    # 发送HEAD请求检查URL是否可达
    try:
        response = requests.head(input_url, timeout=10)
# 增强安全性
        if response.status_code == 200:
# TODO: 优化性能
            return Response("URL is valid and reachable", status=200)
        else:
            return Response("URL is valid but not reachable", status=503)
    except requests.RequestException:
        return Response("URL is unreachable", status=503)
    
@view_config(route_name='validate_url', renderer='json')
def view_validate_url(request):
    # 调用URL验证函数并返回结果
    return validate_url(None, request)