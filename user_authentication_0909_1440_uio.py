# 代码生成时间: 2025-09-09 14:40:05
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.authentication import Authenticated
from pyramid.authorization import Allow
from pyramid.security import remember, forget, authenticated_userid, NO_USER
from pyramid.httpexceptions import HTTPFound
from pyramid.session import check_authorized
from pyramid.settings import asbool
from pyramid.request import Request

# 引入用户模型
from .models import DBSession, User


class MyAuthPolicy(object):
    def authenticated_userid(self, request):
        return request.authenticated_userid

    def effective_principals(self, request):
        return [Authenticated]


# 用户认证视图
@view_config(route_name='login', renderer='json')
def login(request):
    # 获取请求数据
    username = request.params.get('username')
    password = request.params.get('password')

    # 用户身份验证
    if username and password:
        user = DBSession.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            # 登录成功，设置用户身份信息
            headers = remember(request, user.id)
            return {'status': 'success', 'message': 'Login successful'}
        else:
            return {'status': 'error', 'message': 'Invalid username or password'}
    else:
        return {'status': 'error', 'message': 'Missing username or password'}


# 用户登出视图
@view_config(route_name='logout')
def logout(request):
    # 清除用户身份信息
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


# 主程序
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # 添加路由配置
        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        config.add_route('home', '/')

        # 添加视图配置
        config.add_view(login, route_name='login')
        config.add_view(logout, route_name='logout')

        # 添加安全策略
        config.set_auth_policy(MyAuthPolicy())

        # 扫描指定目录以发现视图函数
        config.scan('.views')

    return config.make_wsgi_app()
