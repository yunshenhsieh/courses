from restful_api_server.server import db

class UserModel(db.Model):
    __tablename__ = 'flask_demo_2'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(45))
    username = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self, username, email):
        self.name = username
        self.email = email

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email
        }