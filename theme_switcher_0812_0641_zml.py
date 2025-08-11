# 代码生成时间: 2025-08-12 06:41:41
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.session import check_encrypted
from pyramid.renderers import render_to_response
import json


class MyRootFactory(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='set_theme')
    def set_theme(self):
        """
        Set the theme for the session and return a JSON response.
        """
        try:
            theme = self.request.params['theme']
            if theme:
                self.request.session['theme'] = theme
                return Response(json.dumps({'status': 'success', 'message': 'Theme set successfully'}), content_type='application/json')
            else:
                return Response(json.dumps({'status': 'error', 'message': 'No theme provided'}), content_type='application/json')
        except Exception as e:
            return Response(json.dumps({'status': 'error', 'message': str(e)}), content_type='application/json')

    @view_config(route_name='get_theme')
    def get_theme(self):
        """
        Get the current theme from the session and return a JSON response.
        """
        theme = self.request.session.get('theme', 'default')  # Default theme if not set
        return Response(json.dumps({'status': 'success', 'message': 'Theme retrieved successfully', 'theme': theme}), content_type='application/json')


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_renderer('json')

    # Set a default renderer for the JSON responses
    config.set_default_renderer('json')

    # Add routes and views
    config.add_route('set_theme', '/set_theme')
    config.add_route('get_theme', '/get_theme')
    config.scan()
    return config.make_wsgi_app()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({'here': here}, 
               **{'pyramid.reload_templates': True,
                  'pyramid.debug_all': True,
                  'pyramid.includes': 'pyramid_chameleon'})
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()