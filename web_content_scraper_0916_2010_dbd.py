# 代码生成时间: 2025-09-16 20:10:38
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import requests
from bs4 import BeautifulSoup
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pyramid配置
def main(global_config, **settings):
    """设置Pyramid配置。"""
    config = Configurator(settings=settings)
    config.add_route('scrape', '/scrape')
    config.scan()
    return config.make_wsgi_app()

# 网页内容抓取视图
@view_config(route_name='scrape', renderer='json')
def scrape(request):
    """抓取指定网页的内容。
    参数：
    - request: Pyramid请求对象。
    返回：
    - JSON响应，包含网页内容。
    """
    url = request.params.get('url')
    if not url:
        return {'error': 'URL parameter is required.'}
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        logger.error(f'Request failed: {e}')
        return {'error': 'Request failed.'}
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()  # 获取网页文本内容
        return {'content': content}
    except Exception as e:
        logger.error(f'Failed to parse content: {e}')
        return {'error': 'Failed to parse content.'}

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    logger.info('Serving on http://localhost:6543/...')
    server.serve_forever()