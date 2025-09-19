# 代码生成时间: 2025-09-19 18:39:12
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
import pandas as pd
import numpy as np
from io import StringIO
from pyramid.httpexceptions import HTTPInternalServerError

# 数据统计分析器视图
@view_config(route_name='data_analysis', renderer='json')
def data_analysis(request):
    try:
        # 获取数据文件路径
        data_file_path = request.matchdict['data_file_path']
        
        # 读取数据文件
        df = pd.read_csv(data_file_path)
        
        # 计算基本统计数据
        basic_stats = df.describe()
        
        # 计算缺失值数量
        missing_values = df.isnull().sum()
        
        # 计算相关系数矩阵
        correlation_matrix = df.corr()
        
        # 返回统计数据
        response_body = {
            'basic_stats': basic_stats.to_dict(),
            'missing_values': missing_values.to_dict(),
            'correlation_matrix': correlation_matrix.to_dict()
        }
        return Response(json_body=response_body)
    
    except FileNotFoundError:
        return Response(json_body={'error': '数据文件未找到'}, status=404)
    except pd.errors.EmptyDataError:
        return Response(json_body={'error': '数据文件为空'}, status=400)
    except Exception as e:
        return HTTPInternalServerError(json_body={'error': str(e)})

# 配置Pyramid应用
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        # 配置数据文件路由
        config.add_route('data_analysis', '/data_analysis/{data_file_path}')
        # 配置数据文件视图
        config.scan()

if __name__ == '__main__':
    main({})
