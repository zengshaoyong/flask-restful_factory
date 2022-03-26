import redis
from config import configs, APP_ENV

pool = redis.ConnectionPool(**configs[APP_ENV].REDIS_INFO)
redis_client = redis.Redis(connection_pool=pool)
expires = 3600


def redis_set(key, data):
    data_key = key
    redis_client.set(data_key, data, ex=expires)


def redis_get(key):
    data_key = key
    data = redis_client.get(data_key)
    if data:
        return str(data.decode('utf-8'))
    return None


def redis_delete(key):
    redis_client.delete(key)
