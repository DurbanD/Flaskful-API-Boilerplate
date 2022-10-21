import hashlib
from init import app, db
from Models.User import User

def create():
    email = 'admin@example.com'
    password = 'dbAdmin'
    username = 'admin'
    hashedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    adminUser = User(username=username, password=hashedPass, email=email, admin=True)
    db.session.add(adminUser)
    db.session.commit()