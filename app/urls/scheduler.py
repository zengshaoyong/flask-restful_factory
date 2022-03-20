from flask_restful import Api
from flask import Blueprint

assets_page_scheduler = Blueprint('scheduler', __name__)

api = Api(assets_page_scheduler)
