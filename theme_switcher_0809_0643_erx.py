# 代码生成时间: 2025-08-09 06:43:47
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config

# 配置Session密钥
SECRET = 'yoursecret'
session_factory = SignedCookieSessionFactory(SECRET)

# 主题切换视图
@view_config(route_name='switch_theme', request_method='POST', renderer='json')
def switch_theme(request):
    """
    处理主题切换请求。
    
    参数:
        request: Pyramid的请求对象。
    
    返回:
        一个JSON响应，包含主题切换的结果。
    """
    try:
        # 获取当前选择的主题
        theme = request.params.get('theme')
        
        # 验证主题是否有效
        valid_themes = ['light', 'dark']
        if theme not in valid_themes:
            return {'error': 'Invalid theme'}
        
        # 将主题保存到session
        request.session['theme'] = theme
        
        # 返回成功消息
        return {'success': 'Theme switched to {}'.format(theme)}
    except Exception as e:
        # 错误处理
        return {'error': 'An error occurred: {}'.format(str(e))}

# 配置函数
def main(global_config, **settings):
    """
    Pyramid的配置函数。
    
    参数:
        global_config: 全局配置字典。
        **settings: 其他配置设置。
    """
    config = Configurator(settings=settings)
    
    # 配置静态视图
    config.add_static_view(name='static', path='yourapp:static')
    
    # 配置session工厂
    config.set_session_factory(session_factory)
    
    # 配置路由和视图
    config.add_route('switch_theme', '/switch_theme')
    config.scan()
    
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()