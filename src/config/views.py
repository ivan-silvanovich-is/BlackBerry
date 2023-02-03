from rest_framework import exceptions
from rest_framework.views import exception_handler


def forbidden_to_not_found_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response.status_code == 403:
        response.status_code = 404
        response.data = {'detail': exceptions.NotFound().detail}

    return response
