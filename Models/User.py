from init import db
from time import time
import secrets

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    #Admin Status
    admin = db.Column(db.Boolean)
    # Time created
    created = db.Column(db.Float)
    # Email verification status
    verified = db.Column(db.Boolean)
    # Verification Token generated on init.
    vtoken = db.Column(db.String)
    # Auth is a one-to-many relationship with Session models
    auth = db.relationship('Session', back_populates="user")
    
    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
        self.verified = True if admin == True else False
        self.created = time()
        self.vtoken = str(secrets.token_hex(256))
        self.id = secrets.token_hex(3)
    
    def __repr__(self):
        return f'<User "{self.username}>'