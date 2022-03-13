errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
    # "BadRequest": {
    #     'message': "服务器无法理解您的请求",
    #     'status': 400,
    # },
    "Unauthorized": {
        'message': "您访问的资源未授权或认证已过期",
        'status': 401,
    },
    "Forbidden": {
        'message': "禁止访问",
        'status': 403,
    },
    "NotFound": {
        'message': "您访问的资源不存在",
        'status': 404,
    },
    "MethodNotAllowed": {
        'message': "请求方式不被允许",
        'status': 405,
    },
    "RequestTimeout": {
        'message': "请求超时",
        'status': 408,
    },
}
