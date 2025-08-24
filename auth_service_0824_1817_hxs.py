# 代码生成时间: 2025-08-24 18:17:31
# auth_service.py

"""
This module provides a simple user authentication service.
It handles user login and logout functionality.
"""

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config

# Assuming a simple in-memory user database for demonstration purposes
users = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'user': {'password': 'userpass', 'role': 'user'},
}

# Function to check user credentials
def check_credentials(username, password, users):
    user = users.get(username)
    if user and user['password'] == password:
        return user['role']
    return None

# Pyramid authentication callback
def auth_callback(username, password, request):
    role = check_credentials(username, password, users)
    if role:
        return role
    return None

# Pyramid logout callback
def remember(request, username, **kw):
    return {'username': username}

def forget(request):
    request.response.set_cookie('auth_tkt', '', max_age=0)
    return {}

# Pyramid view to handle login
@view_config(route_name='login', renderer='string')
def login(request):
    if request.method == 'POST':
        username = request.params.get('username')
        password = request.params.get('password')
        if check_credentials(username, password, users):
            headers = remember(request, username)
            return 'Logged in as %s' % username
        else:
            request.response.status = 401
            return 'Login failed'
    else:
        return 'Please log in'

# Pyramid view to handle logout
@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return 'Logged out'

# Function to create a Pyramid WSGI application
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.

    :param global_config: The global configuration settings.
    :param settings: The configuration settings specific to this application.
    :return: A Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # Setup authentication policy
        authn_policy = AuthTktAuthenticationPolicy('a_shared_secret')
        config.set_authentication_policy(authn_policy)

        # Setup authorization policy
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

        # Setup session factory
        session_factory = SignedCookieSessionFactory('a_secret')
        config.set_session_factory(session_factory)

        # Add views
        config.add_route('login', '/login')
        config.add_view(login, route_name='login')
        config.add_route('logout', '/logout')
        config.add_view(logout, route_name='logout')

        # Scan for @view_config decorated view functions
        config.scan()

    return config.make_wsgi_app()