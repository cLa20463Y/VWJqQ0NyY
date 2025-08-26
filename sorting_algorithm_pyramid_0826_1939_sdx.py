# 代码生成时间: 2025-08-26 19:39:27
# Pyramid框架是一个基于python的web框架，这里我们实现一个排序算法的服务。

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.exceptions import NotFound

# 定义排序算法
def bubble_sort(arr):
    """冒泡排序，简单的排序算法"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    """插入排序，简单高效的排序算法"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = key
    return arr

def selection_sort(arr):
    """选择排序，简单直观的排序算法"""
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Pyramid视图配置
@view_config(route_name='sort', renderer='json')
def sort_view(request):
    # 获取请求参数
    data = request.json_body
    if not data:
        return Response(json_body={'error': 'No data provided'}, status=400)

    # 检查数据类型
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        return Response(json_body={'error': 'Invalid data type'}, status=400)

    # 执行排序算法
    try:
        sorted_data = bubble_sort(data.copy())  # 使用冒泡排序
        # sorted_data = insertion_sort(data.copy())  # 可以使用插入排序
        # sorted_data = selection_sort(data.copy())  # 可以使用选择排序
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

    # 返回排序结果
    return {'sorted_data': sorted_data}

# 配置Pyramid应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('sort', '/sort')
    config.scan()
    return config.make_wsgi_app()

# 运行Pyramid应用
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()