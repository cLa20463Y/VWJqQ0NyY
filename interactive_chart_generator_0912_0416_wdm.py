# 代码生成时间: 2025-09-12 04:16:45
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
import json

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs

# 配置Pyramid应用
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')  # 支持渲染Chameleon模板
    config.add_route('index', '/')  # 添加路由
    config.scan()  # 扫描装饰器
    return config.make_wsgi_app()

# 视图函数
@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    # 创建图表
    p = figure(title="Interactive Chart", x_axis_label='x', y_axis_label='y')
    p.line(x=[1, 2, 3, 4, 5], y=[6, 7, 2, 4, 5])
    
    # 添加数据源和悬停工具
    source = ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[6, 7, 2, 4, 5]))
    hover = HoverTool(tooltips=[("x", "@x"), ("y", "@y")])
    p.add_tools(hover)
    p.add_layout(source)
    
    # 将图表和数据源转换为HTML和JS代码
    script, div = components(p)
    
    # 渲染模板并返回响应
    return render_to_response('index.pt', {'bokeh_script': script, 'bokeh_div': div}, request)

# 应用结构
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 6543, main).serve_forever()