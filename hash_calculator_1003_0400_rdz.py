# 代码生成时间: 2025-10-03 04:00:21
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import hashlib

# 定义一个哈希值计算工具的视图函数
@view_config(route_name='hash_calculator', renderer='json')
def hash_calculator(request):
    """
    哈希值计算工具视图函数。
    
    该函数接受输入的字符串，返回其MD5、SHA1和SHA256哈希值。
    
    :param request: Pyramid请求对象。
    :return: 包含哈希值的JSON响应。
    """
    try:
        # 从请求中获取要计算哈希值的字符串
        input_string = request.matchdict['string']
    except KeyError:
        # 如果请求中没有提供字符串，则返回错误信息
        return Response(json_body={'error': 'No input string provided.'}, status=400)
    
    # 创建一个字典来存储不同的哈希值
    hash_values = {} 
    
    # 计算MD5哈希值
    hash_values['md5'] = hashlib.md5(input_string.encode()).hexdigest() 
    
    # 计算SHA1哈希值
    hash_values['sha1'] = hashlib.sha1(input_string.encode()).hexdigest() 
    
    # 计算SHA256哈希值
    hash_values['sha256'] = hashlib.sha256(input_string.encode()).hexdigest() 
    
    return hash_values

# Pyramid配置器，用于配置视图和路由
def main(global_config, **settings):
    """
    Pyramid配置器。
    
    该函数配置了视图和路由，使哈希值计算工具可用。
    
    :param global_config: Pyramid全局配置。
    :param settings: 额外的配置设置。
    """
    with Configurator(settings=settings) as config:
        # 添加路由和视图
        config.add_route('hash_calculator', '/hash/{string}')
        config.scan()

# 允许直接运行此文件以启动服务器
if __name__ == '__main__':
    main({})
