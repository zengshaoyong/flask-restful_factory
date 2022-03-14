from flask import Flask
from config import configs, APP_ENV
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_cors import CORS
from app.common.logging import Logger
from flask_caching import Cache
from datetime import timedelta
from flask_session import Session

# 设置访问限制
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120 per minute", "10 per second"],
)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()


# 工厂函数
def create_app():
    app = Flask(__name__)
    app.config.from_object(configs[APP_ENV])
    # 注册数据库
    db.init_app(app)
    migrate.init_app(app, db)
    # 跨域设置
    CORS(app, supports_credentials=True)
    # session设置
    app.permanent_session_lifetime = timedelta(minutes=30)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    # 开启缓存
    cache.init_app(app)
    # 注册session
    Session(app)
    # 初始化日志格式
    logger = Logger()
    logger.init_app(app)
    # 注册访问限制
    limiter.init_app(app)

    return app
