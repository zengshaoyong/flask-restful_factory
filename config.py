import redis

APP_ENV = "test"


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_RECYCLE = 3600
    SECRET_KEY = 'How do you turn this on?'
    CACHE_TYPE = 'redis'
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = False
    SESSION_KEY_PREFIX = "session:"


class Development(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456789@localhost:3306/flask"


class Test(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456789@localhost:3306/flask'
    REDIS_INFO = {'host': '127.0.0.1', 'port': 6379, 'password': 123456789}
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password='123456789', db=1)
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 123456789
    CACHE_REDIS_DB = 2
    CACHE_DEFAULT_TIMEOUT = 300
    DEBUG = True


class Product(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456789@localhost:3306/flask'


configs = {
    'dev': Development,
    'test': Test,
    'pro': Product,
}
