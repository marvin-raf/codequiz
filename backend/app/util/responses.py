"""
Contains responses
"""

from flask import jsonify


def response(status_code, data=None):
    """
    Generic response with status code
    """

    if data:
        return (jsonify({"data": data}), status_code)

    return ("", status_code)


def success(data=None):
    """
    Success response with 200 status
    """
    return response(data, 200)


def created(data=None):
    """
    Created response with 201 status
    """
    return response(data, 201)


def bad_request(data=None):
    """
    Bad Request response with 400 status 
    """
    return response(data, 400)


def unauthorized(data=None):
    """
    Unauthorized response with 401 status
    """
    return response(data, 401)


def forbidden(data=None):
    """
    Forbidden response with 403 status
    """
    return response(data, 403)


def not_found(data=None):
    """
    Not Found response with 404 status
    """
    return response(data, 404)


def server_error(data=None):
    """
    Server Error response with 500 status
    """

    return response(data, 500)
