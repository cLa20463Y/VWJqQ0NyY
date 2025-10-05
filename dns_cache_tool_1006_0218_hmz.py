# 代码生成时间: 2025-10-06 02:18:22
from pyramid.config import Configurator
from pyramid.view import view_config
import dns.resolver
from dns.exception import DNSException
import logging
import cachetools.func


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 设置缓存函数，缓存时长为60秒
@cachetools.func.ttl_cache(maxsize=100, ttl=60)
def resolve_dns(domain: str) -> str:
    """
    DNS解析函数，使用缓存来减少对DNS服务器的请求
    :param domain: 需要解析的域名
    :return: 解析得到的IP地址
    """
    try:
        answer = dns.resolver.resolve(domain, 'A')
        return answer[0].to_text()
    except (DNSException, IndexError) as e:
        logger.error(f"DNS解析失败: {e}")
        raise Exception(f"DNS解析失败: {e}")


# Pyramid视图配置
def dns_view(request):
    """
    用于处理HTTP请求，解析域名
    :param request: Pyramid请求对象
    :return: JSON响应
    """
    domain = request.matchdict['domain']
    try:
        ip = resolve_dns(domain)
        return {
            'status': 'success',
            'ip': ip,
            'message': f'{domain} has been resolved to {ip}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


# Pyramid配置
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('dns', '/dns/{domain}')
        config.add_view(dns_view, route_name='dns', renderer='json')
        config.scan()


# 如果直接运行，将调用main函数启动程序
if __name__ == '__main__':
    main()
