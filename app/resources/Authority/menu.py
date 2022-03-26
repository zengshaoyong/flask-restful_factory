from flask_restful import Resource
from app import limiter
from app.utils.databases.user import get_authority
from flask_login import login_required, current_user
from app.utils.redis import redis_set, redis_get
import json
import re


def get_menu(username):
    paths = get_authority(username)
    routes, master, slave = [], [], []
    for i in paths:
        if i.count('/') == 1:
            master.append(i)
        if i.count('/') == 2:
            slave.append(i)
    for i in master:
        route = {'path': str(i)}
        children = []
        for j in slave:
            if i == re.match('/\\w+', j).group():
                children.append({'path': str(j)})
        route['children'] = children
        routes.append(route)

    return routes


class Menu(Resource):
    decorators = [limiter.limit(limit_value="1 per second", key_func=lambda: current_user.id,
                                error_message='访问太频繁'), login_required]

    @staticmethod
    def get():
        cache = redis_get(current_user.id + '_menu')
        if cache is None:
            menu = get_menu(current_user.id)
            redis_set(current_user.id + '_menu', json.dumps(menu))
            return {'data': menu}
        else:
            return {'data': json.loads(cache)}
