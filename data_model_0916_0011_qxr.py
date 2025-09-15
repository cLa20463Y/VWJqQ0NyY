# 代码生成时间: 2025-09-16 00:11:14
# data_model.py

"""
This module defines the data models for our Pyramid application.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyramid.config import Configurator
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import create_engine
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

# Initialize the declarative base
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    
    def __init__(self, name, email, age=None):
        self.name = name
        self.email = email
        self.age = age
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', age={self.age})>"

# Define the database engine and sessionmaker
engine = create_engine('sqlite:///pyramid_model.db')
Session = sessionmaker(bind=engine)

# Function to initialize the database
def init_db():
    """
    Initialize the database by creating all tables that are defined by the Base class.
    """
    Base.metadata.create_all(engine)

# Example Pyramid configuration function
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    
    # Set up authentication and authorization
    authn_policy = CallbackAuthenticationPolicy(callback)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authn_policy(authn_policy)
    config.set_authz_policy(authz_policy)
    
    # Register the models
    config.registry['dbsession'] = sessionmaker(bind=engine)
    
    # Add a route for the index page
    config.add_route('index', '/')
    
    # Scan for @view_config decorated views
    config.scan()
    
    return config.make_wsgi_app()

# Callback function for authentication
def callback(username, password, request):
    """
    Callback function for authentication. This should check the provided credentials
    against our data store and return True if they are valid, False otherwise.
    """
    session = request.registry['dbsession']()
    user = session.query(User).filter_by(email=username).first()
    return user and user.age > 18 # Example condition
    
# Set up logging
setup_logging('pyramid.ini')
settings = get_appsettings('pyramid.ini', name='main')

# Initialize the database
init_db()

# Call the main function to set up the Pyramid app
app = main(settings)

# The if __name__ == '__main__' block allows us to run this script directly
# to test the Pyramid application.
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('0.0.0.0', 6543, app)
    srv.serve_forever()