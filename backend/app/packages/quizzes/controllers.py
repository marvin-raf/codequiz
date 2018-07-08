from flask import Blueprint, request, abort, jsonify
from app.packages.quizzes import models
from app.util.responses import success, bad_request, server_error, created, forbidden
from app.util.middleware import teacher_signed_in

quizzes_module = Blueprint("quizzes", __name__, url_prefix="/quizzes")
