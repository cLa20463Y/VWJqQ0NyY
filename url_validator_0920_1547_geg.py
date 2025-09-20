# 代码生成时间: 2025-09-20 15:47:07
# url_validator.py - A Pyramid application to validate URL links.

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import requests
from urllib.parse import urlparse

# Define the URL Validator view class
class URLValidator:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='validate_url', renderer='json')
    def validate_url(self):
        # Get the URL from the request parameters
        url = self.request.params.get('url')

        # Check if the URL is provided
        if not url:
            return {
                'error': 'URL parameter is missing.'
            }

        try:
            # Parse the URL to validate its format
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError('Invalid URL format.')

            # Check if the URL is reachable
            response = requests.head(url, timeout=5)
            if response.status_code != 200:
                raise ValueError('URL is not reachable.')

            # If all checks pass, the URL is valid
            return {
                'status': 'success',
                'message': 'URL is valid.',
                'url': url,
            }
        except ValueError as e:
            # Return the error message if validation fails
            return {
                'status': 'error',
                'message': str(e),
            }
        except requests.RequestException as e:
            # Handle any request exceptions, such as connection errors
            return {
                'status': 'error',
                'message': 'Failed to reach the URL.',
            }

# Initialize the Pyramid configuration
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        # Add the URL Validator view
        config.add_route('validate_url', '/validate')
        config.scan()

if __name__ == '__main__':
    main({})