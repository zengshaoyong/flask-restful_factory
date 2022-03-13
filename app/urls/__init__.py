from flask import Blueprint

assets_page = Blueprint('assets_page', __name__)

from .apis import api
