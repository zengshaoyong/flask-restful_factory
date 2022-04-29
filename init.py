from app import db
from app import create_app
from app.models.db import User

db.app = create_app()

new_user = User(username='zsy', password='123456789', current_authority='admin')
db.session.add(new_user)
db.session.commit()
db.session.close()
