from flask_login import UserMixin
from app.app import db, login_manager


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def get_id(self):
        return self.id_user

    def __repr__(self):
        return f"<User: {self.username}, E-mail: {self.email}>"
