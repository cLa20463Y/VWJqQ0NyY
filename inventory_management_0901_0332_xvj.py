# 代码生成时间: 2025-09-01 03:32:12
# inventory_management.py
"""
库存管理系统使用PYRAMID框架实现。
该系统提供基本的库存管理功能，包括添加、删除、更新和查询库存项。
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPInternalServerError
from pyramid.renderers import render_to_response
from pyramid.security import has_permission
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactoryConfig

from sqlalchemy import create_engine, Column, Integer, String, Float, Sequence, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, session
from zope.sqlalchemy import register

# 数据库配置
DATABASE_URL = 'sqlite:///inventory.db'

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建基类
Base = declarative_base()

# 定义库存项表
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, Sequence('inventory_item_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<InventoryItem(name='{self.name}', quantity={self.quantity}, price={self.price})>"

# 初始化数据库表
Base.metadata.create_all(engine)

# 创建会话工厂
SessionFactory = sessionmaker(bind=engine)

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # 设置身份验证和授权策略
    auth_policy = AuthTktAuthenticationPolicy('secret_key')
    authz_policy = ACLAuthorizationPolicy()
    config.set_auth_policy(auth_policy)
    config.set_authorization_policy(authz_policy)
    
    # 设置会话工厂
    config.set_session_factory(SessionFactory)
    config.add_session_cleanup()
    
    # 路由和视图配置
    config.add_route('home', '/')
    config.add_route('add_item', '/add')
    config.add_route('update_item', '/update/{id}')
    config.add_route('delete_item', '/delete/{id}')
    config.add_route('view_item', '/view/{id}')
    
    config.scan()
    return config.make_wsgi_app()

# 视图函数
@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    """
    首页视图，显示库存列表。
    """
    session = request.dbSession
    items = session.query(InventoryItem).all()
    return {'items': items}

@view_config(route_name='add_item', renderer='templates/add_item.jinja2')
def add_item_view(request):
    """
    添加库存项视图。
    """
    if request.method == 'POST':
        name = request.params.get('name')
        quantity = int(request.params.get('quantity'))
        price = float(request.params.get('price'))
        try:
            new_item = InventoryItem(name, quantity, price)
            session = request.dbSession
            session.add(new_item)
            session.commit()
            return HTTPFound(location=request.route_url('home'))
        except Exception as e:
            request.session.flash(f'Error adding item: {e}', 'error')
    return {'error': 'Invalid form submission'}

@view_config(route_name='update_item', renderer='templates/update_item.jinja2')
def update_item_view(request):
    """
    更新库存项视图。
    """
    item_id = request.matchdict['id']
    if request.method == 'POST':
        name = request.params.get('name')
        quantity = int(request.params.get('quantity'))
        price = float(request.params.get('price'))
        try:
            session = request.dbSession
            item = session.query(InventoryItem).get(item_id)
            item.name = name
            item.quantity = quantity
            item.price = price
            session.commit()
            return HTTPFound(location=request.route_url('home'))
        except Exception as e:
            request.session.flash(f'Error updating item: {e}', 'error')
    session = request.dbSession
    item = session.query(InventoryItem).get(item_id)
    return {'item': item}

@view_config(route_name='delete_item', renderer='json')
def delete_item_view(request):
    """
    删除库存项视图。
    """
    item_id = request.matchdict['id']
    try:
        session = request.dbSession
        item = session.query(InventoryItem).get(item_id)
        if item:
            session.delete(item)
            session.commit()
            return Response(json_body={'message': 'Item deleted successfully'}, content_type='application/json')
        else:
            return Response(json_body={'error': 'Item not found'}, content_type='application/json', status=404)
    except Exception as e:
        return Response(json_body={'error': f'Error deleting item: {e}'}, content_type='application/json', status=500)

@view_config(route_name='view_item', renderer='templates/view_item.jinja2')
def view_item_view(request):
    """
    查看库存项视图。
    """
    item_id = request.matchdict['id']
    session = request.dbSession
    item = session.query(InventoryItem).get(item_id)
    if item:
        return {'item': item}
    else:
        return HTTPFound(location=request.route_url('home'))
