# 代码生成时间: 2025-08-05 07:51:28
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.view import view_config
import os

# 配置文件，用于设置金字塔的基本参数和访问控制
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 设置密钥
    auth_secret = os.environ.get('AUTH_SECRET')
    
    # 设置认证策略
    auth_policy = AuthTktAuthenticationPolicy('mysecret')
    auth_policy.hashalg = 'sha512'
    
    # 设置授权策略
    authz_policy = ACLAuthorizationPolicy()
    
    # 加载视图
    config.include('.views')
    
    # 配置视图访问控制
    config.set_authorization_policy(authz_policy)
    config.set_authentication_policy(auth_policy)
    
    # 启动应用
    return config.make_wsgi_app()

# 视图模块
from pyramid.response import Response

# 公共视图
class PublicView:
    @view_config(route_name='public', request_method='GET')
    def public_view(self):
        """
        一个公共视图，不需要认证和授权
        """
        return Response('任何人都可以看到这个视图')

# 私有视图
class PrivateView:
    @view_config(route_name='private', request_method='GET', permission='view')
    def private_view(self):
        """
        一个私有视图，需要认证和授权
        """
        return Response('只有被授权的用户可以看到这个视图')

# 视图配置
def includeme(config):
    """
    配置视图
    """
    config.scan('.views', include='.views')

# 运行配置文件
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('' , 6543, main) as server:
        print("服务器运行在 http://localhost:6543/")
        server.serve_forever()