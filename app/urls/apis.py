from flask_restful import Api
from app.common.errors import errors
from app.resources.Test.test import HelloWorld
from app.resources.Authority.auth import Login, Logout
from flask import Blueprint

assets_page = Blueprint('assets_page', __name__)

api = Api(assets_page, errors=errors, catch_all_404s=True)

api.add_resource(HelloWorld, '/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
