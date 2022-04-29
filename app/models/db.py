from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(255), nullable=False)
    currentAuthority = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, current_authority):
        self.username = username
        self.password = generate_password_hash(password)
        self.currentAuthority = current_authority

    # 定义一个修改密码和方法

    def update_password(self, pwd):
        self.password = generate_password_hash(pwd)
        db.commit()

    # 定义一个修改权限和方法

    def update_authority(self, authority):
        self.currentAuthority = authority
        db.commit()

    # 定义一个验证密码的方法

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
