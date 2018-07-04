from flask import Blueprint, jsonify
from app.util.db import query
courses_module = Blueprint("courses", __name__, url_prefix="/courses")


@courses_module.route("/")
def helloworld():
    """
    Print hello world
    """
    data = query("SELECT 1+1")
    return jsonify(data)
