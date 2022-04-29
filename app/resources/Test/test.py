from flask_restful import Resource, reqparse
from flask_login import login_required


class HelloWorld(Resource):
    decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, help='用户名参数验证失败', required=True)
        self.args = self.parser.parse_args()

    @staticmethod
    def get():
        return {'data': "hello world", 'message': 'test'}
