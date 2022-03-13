from app import db
from app.models.db import User
from werkzeug.security import generate_password_hash


def query_user(username):
    return User.query.filter(User.username == username).first()


def create_user(username, password, current_authority):
    new_user = User(username=username, password=password, current_authority=current_authority)
    db.session.add(new_user)
    db.session.commit()
    db.session.close()


def modify_user(username, password, current_authority):
    user = query_user(username)
    user.password = generate_password_hash(password)
    user.currentAuthority = current_authority
    db.session.commit()
    db.session.close()


def delete_user(username):
    user = query_user(username)
    db.session.delete(user)
    db.session.commit()
    db.session.close()


def get_authority(username):
    user = query_user(username)
    paths = user.currentAuthority.split(',')
    return paths
