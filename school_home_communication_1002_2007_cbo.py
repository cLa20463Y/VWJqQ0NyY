# 代码生成时间: 2025-10-02 20:07:37
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory

# 数据库模型（假设使用SQLAlchemy ORM）
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 配置数据库连接
engine = create_engine('sqlite:///school_home_communication.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 定义用户和消息模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    messages = relationship('Message', back_populates='author')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='messages')

# 创建数据库表
Base.metadata.create_all(engine)

# 配置Pyramid应用程序
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 配置安全和会话
    config.set_authentication_policy(AuthTktAuthenticationPolicy('secret'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    session_factory = SignedCookieSessionFactory('another-secret')
    config.set_session_factory(session_factory)
    
    # 配置路由和视图
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('create_message', '/create_message')
    
    config.scan()
    return config.make_wsgi_app()

# 视图函数
@view_config(route_name='home', renderer='json')
def home_view(request):
    """
    主页视图：显示所有消息
    """
    session = Session()
    messages = session.query(Message).all()
    return {'messages': [{'id': message.id, 'content': message.content, 'author': message.author.name} for message in messages]}

@view_config(route_name='login', renderer='json')
def login_view(request):
    """
    登录视图：验证用户身份并返回令牌
    """
    # 登录逻辑（省略）
    pass

@view_config(route_name='logout', renderer='json')
def logout_view(request):
    """
    登出视图：清除会话
    """
    request.session.invalidate()
    return {}

@view_config(route_name='create_message', renderer='json')
def create_message_view(request):
    """
    创建消息视图：创建新消息并存储到数据库
    """
    session = Session()
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    
    if content is None or user_id is None:
        return {'error': 'Invalid input'}
    
    new_message = Message(content=content, author_id=user_id)
    session.add(new_message)
    session.commit()
    return {'message': {'id': new_message.id, 'content': new_message.content, 'author': new_message.author.name}}
