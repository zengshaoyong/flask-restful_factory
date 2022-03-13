from flask_restful import Resource, abort, reqparse
from flask import jsonify, current_app
from flask_login import current_user, login_required
from werkzeug import exceptions
from app import cache


class HelloWorld(Resource):
    decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='用户名参数验证失败', required=True)
        self.args = self.parser.parse_args()

    def get(self):
        print(current_user)
        current_app.logger.info('测试')
        return {'message': "hello world"}, 201
