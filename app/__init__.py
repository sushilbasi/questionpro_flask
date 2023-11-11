from flask import Blueprint

app_bp = Blueprint('api', __name__)

from . import views
