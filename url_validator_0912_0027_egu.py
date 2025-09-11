# 代码生成时间: 2025-09-12 00:27:20
from urllib.parse import urlparse
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
import requests

"""
This module contains a Pyramid view function that validates the URL provided in the request's query string.
It checks if the URL is well-formed and if it can be accessed (HTTP 200 status code).
"""


@view_config(route_name='validate_url', request_method='GET')
def validate_url(request):
    """
    Validate the URL provided in the query string of the request.
    
    :param request: The Pyramid request object.
    :return: A Pyramid response object with the validation result.
    """
    # Get the URL from the query string
    url_to_validate = request.params.get('url')
    
    # Check if the URL was provided
    if not url_to_validate:
        return HTTPBadRequest('No URL provided. Please provide a URL in the query string.')
    
    try:
        # Parse the URL to check if it's well-formed
        parsed_url = urlparse(url_to_validate)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return HTTPBadRequest('Invalid URL format. Please provide a well-formed URL.')
        
        # Try to access the URL to check its validity
        response = requests.head(url_to_validate, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return Response('URL is valid and accessible.')
        else:
            return Response(f'URL is valid but not accessible: {response.status_code}', status=response.status_code)
    except requests.RequestException as e:
        return HTTPInternalServerError(f'An error occurred while accessing the URL: {e}')
    except Exception as e:
        return HTTPInternalServerError(f'An unexpected error occurred: {e}')
