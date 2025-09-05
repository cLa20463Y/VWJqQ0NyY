# 代码生成时间: 2025-09-06 05:58:10
from pyramid.config import Configurator
# TODO: 优化性能
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
# 添加错误处理
from pyramid.view import view_config
# 优化算法效率
from pyramid.security import Allow, Everyone, Authenticated

# 数据库模型初始化
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 配置数据库连接
engine = create_engine('sqlite:///users.db')
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# 初始化数据库表
# 扩展功能模块
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Pyramid配置
# 优化算法效率
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.set_root_factory('pyramid_chameleon.zpt.view_root_factory')
        config.include('pyramid_chameleon.zpt')
        config.include('.models')  # 加载数据库模型

        # 配置认证策略
        authn_policy = AuthTktAuthenticationPolicy(
            callback=groupfinder,
            hashalg='sha512',
            secret='secret!'
        )
        config.set_authentication_policy(authn_policy)

        # 配置授权策略
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

        # 配置会话工厂
        session_factory = SignedCookieSessionFactory('another-secret!')
        config.set_session_factory(session_factory)

        # 添加登录视图
# 改进用户体验
        config.add_route('login', '/login')
        config.scan()
# 增强安全性

# 用户查找函数
def get_user(username):
    session = Session()
    try:
        return session.query(User).filter_by(username=username).one()
    finally:
        session.close()

# 用户组查找函数
# 改进用户体验
def groupfinder(userid, request):
    user = get_user(userid)
    if user is not None:
        return [Authenticated]
    return [Everyone]

# 登录视图
@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    username = request.params.get('username')
    password = request.params.get('password')

    if request.method == 'POST':
        user = get_user(username)
        if user and user.password == password:
            headers = remember(request, username)
            return HTTPFound(location='/', headers=headers)
        else:
            request.session.flash('Invalid username or password')

    return {}

# 登记用户函数
def remember(request, username, **kw):
    # Use the 'username' identity to represent this user
# TODO: 优化性能
    headers = request.response.headers
    headers.add('Set-Cookie',
# 扩展功能模块
                'login=%s; Path=/; HttpOnly' % request.auth_token)
    return headers

if __name__ == '__main__':
    main({"__file__": __file__})
