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
    return response(200, data)


def created(data=None):
    """
    Created response with 201 status
    """
    return response(201, data)


def bad_request(data=None):
    """
    Bad Request response with 400 status 
    """
    return response(400, data)


def unauthorized(data=None):
    """
    Unauthorized response with 401 status
    """
    return response(401, data)


def forbidden(data=None):
    """
    Forbidden response with 403 status
    """
    return response(403, data)


def not_found(data=None):
    """
    Not Found response with 404 status
    """
    return response(404, data)


def server_error(data=None):
    """
    Server Error response with 500 status
    """

    return response(500, data)
