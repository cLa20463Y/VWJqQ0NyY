# 代码生成时间: 2025-08-07 14:31:39
from pyramid.view import view_config
from pyramid.response import Response
import random

# 定义一个视图函数，用于生成随机数
@view_config(route_name='random_number', renderer='json')
def random_number_view(request):
    # 获取请求参数
    try:
        lower_limit = int(request.params.get('lower', 0))
        upper_limit = int(request.params.get('upper', 100))
    except ValueError:
        # 如果请求参数不是整数，返回错误信息
        return Response(
            "Invalid input: 'lower' and 'upper' must be integers.",
            content_type='text/plain',
            status=400)
    
    # 检查边界值是否有效
    if lower_limit >= upper_limit:
        return Response(
            "Invalid input: 'lower' must be less than 'upper'.",
            content_type='text/plain',
            status=400)
    
    # 生成随机数
    random_number = random.randint(lower_limit, upper_limit)
    
    # 返回随机数
    return {"random_number": random_number}

# 错误处理函数
@view_config(context=Exception, renderer='json')
def error_view(exc, request):
    "