from app.models.user import User
from app import login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource, reqparse
from flask import session, abort
from app.utils.redis import redis_set, redis_get
from flask_limiter.util import get_remote_address
from app.utils.databases.user import query_user
from flask import current_app
from app import limiter


@login_manager.user_loader
def load_user(username):
    curr_user = None
    if redis_get('user' + '_' + username):
        curr_user = User()
        curr_user.id = username
    elif query_user(username):
        curr_user = User()
        curr_user.id = username
        redis_set('user' + '_' + username, 'True')
    return curr_user


# 未登录的直接返回401
@login_manager.unauthorized_handler
def unauthorized_handler():
    abort(401)


class Login(Resource):
    decorators = [limiter.limit(limit_value='1 per second', key_func=get_remote_address,
                                error_message="访问太频繁")]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('passWord', required=True, help="密码不能为空")
        self.parser.add_argument('userName', required=True, help="用户名不能为空")
        self.parser.add_argument('type')
        self.args = self.parser.parse_args()

    def post(self):
        username = self.args['userName']
        password = self.args['passWord']
        user = query_user(username)
        if user is None:
            return {'message': '用户不存在'}
        if user.check_password(password):
            curr_user = User()
            curr_user.id = username
            login_user(curr_user)
            session.permanent = True
            current_app.logger.info(username + "登陆成功")
            return {'message': '登录成功', 'status': 'AuthenticationOk'}
        return {'message': '密码错误'}


class Logout(Resource):
    decorators = [limiter.limit(limit_value="1 per second", key_func=get_remote_address,
                                error_message='访问太频繁'), login_required]

    @staticmethod
    def post():
        username = current_user.id
        logout_user()
        return {'message': '{} logout successfully'.format(username)}


# 获取当前用户的信息
class CurrentUser(Resource):
    decorators = [limiter.limit(limit_value="2 per second", key_func=lambda: current_user.id,
                                error_message='访问太频繁'), login_required]

    @staticmethod
    def get():
        return {'name': current_user.id}
