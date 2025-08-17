# 代码生成时间: 2025-08-18 03:36:40
import logging
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库配置
DATABASE_URL = "postgresql://user:password@localhost/dbname"  # 替换为你的数据库配置

class DBSessionFactory(object):
    """创建数据库会话工厂"""
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = None
        self.session_factory = None

    def get_engine(self):
        """获取数据库引擎"""
        if self.engine is None:
            self.engine = create_engine(self.database_url)
        return self.engine

    def get_session(self, scoped=True):
        """获取数据库会话"""
        if scoped:
            if self.session_factory is None:
                self.session_factory = scoped_session(sessionmaker(bind=self.get_engine()))
            return self.session_factory()
        else:
            return self.session_factory()

    def close_all_sessions(self):
        """关闭所有会话"""
        if self.session_factory:
            self.session_factory.remove()

# Pyramid配置
def main(global_config, **settings):
    """设置Pyramid配置"""
    with Configurator(settings=settings) as config:
        config.include('pyramid_tm')  # 启用事务管理
        config.registry.settings['sqlalchemy.url'] = DATABASE_URL
        config.registry.session_factory = DBSessionFactory(DATABASE_URL)
        config.scan()

if __name__ == '__main__':
    main({})