from init import db
from time import time

class User(db.Model):
    __tablename__= "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    admin = db.Column(db.Boolean)
    created = db.Column(db.Float)
    verified = db.Column(db.Boolean)
    
    auth = db.relationship('Session', back_populates="user")
    
    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        self.verified = True if admin == True else False
        self.created = time()
    
    def __repr__(self):
        return f'<User "{self.username}>'