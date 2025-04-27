from app.app import db


class Post(db.Model):
    __tablename__ = "posts"

    id_post = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id_user'))

    def __repr__(self):
        return f"<Body: {self.body}, Created_at: {self.created_at}, User_Id: {self.user_id}>"