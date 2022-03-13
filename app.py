from gevent import monkey

monkey.patch_all()

from app import create_app, migrate
from app.urls import assets_page
from gevent.pywsgi import WSGIServer
from app.models.db import db

app = create_app()
db.create_all(app=app)
# 注册蓝本
app.register_blueprint(assets_page)

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
