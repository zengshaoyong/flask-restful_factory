import mysql.connector
from DBUtils.PooledDB import PooledDB
from elasticsearch import Elasticsearch


class DbConnection(object):
    def __init__(self, database):
        self.__pool = PooledDB(creator=mysql.connector, mincached=1, maxcached=20, host=database.ip,
                               port=database.port, user=database.user, passwd=database.password,
                               db=database.target, charset=database.charset, auth_plugin='mysql_native_password')
        self.__cs = self.__pool.connection().cursor()

    def __enter__(self):
        return self.__cs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cs.close()
        self.__pool.close()


class EsConnection(object):
    def __init__(self, database):
        self.__es = Elasticsearch(hosts='http://' + database.ip, port=database.port,
                                  http_auth=(database.user, database.password),
                                  timeout=3600)

    def __enter__(self):
        return self.__es

    def __exit__(self, exc_type, exc_val, exc_tb):
        return
