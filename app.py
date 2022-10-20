import json
from types import NoneType
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import hashlib
import os
import time
import secrets
from Tools.emailValidator import validate

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DB
db = SQLAlchemy(app)

#Init Marshmallow
ma = Marshmallow(app)

# User Model
class User(db.Model):
    __tablename__= "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    admin = db.Column(db.Boolean)
    
    auth = db.relationship('Session', back_populates="user")
    
    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin
    
    def __repr__(self):
        return f'<User "{self.username}>'

# Session Model
class Session(db.Model):
    __tablename__="session"
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    user = db.relationship("User", back_populates="auth", uselist=False)
    
    agent = db.Column(db.String)
    issued = db.Column(db.Float)
    access_token = db.Column(db.String, unique = True)
    access_expiration = db.Column(db.Float)
    refresh_token = db.Column(db.String, unique = True)
    refresh_expiration = db.Column(db.Float)
    
    def __init__(self, agent):
        self.generateTokens()
        self.agent = agent
    def generateTokens(self):
        issued = time.time()
        sessionToken = secrets.token_hex(256)
        refreshToken = secrets.token_hex(256)
        
        session_exp = time.time() + 300
        # 300 seconds is 5 minutes
        refresh_exp = time.time() + 259200
        # 2592000 seconds is 30 days
        
        self.issued = issued
        self.access_token  = sessionToken
        self.access_expiration = session_exp
        self.refresh_token = refreshToken
        self.refresh_expiration = refresh_exp

#Schema
class SessionSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'issued', 'access_token', 'access_expiration', 'refresh_token', 'refresh_expiration', 'agent')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'admin')

        
#Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

### Routes

## /user/
# Create User
@app.route('/user', methods=['POST'])
def add_user():
    try:
        email = request.json['email']
        username = request.json['username']
        userAgent = request.headers['User-Agent']
        hashedPass = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
    except:
        return Response(status=400)
    if validate(email) == False:
        return Response(status=400)
    
    # Create the User
    new_user = User(username=username, password=hashedPass, email=email)
    
    # Create New Session and Set Information
    new_session = Session(userAgent)
    new_session.user = new_user
    
    # Make the Changes
    db.session.add(new_user)
    db.session.add(new_session)
    db.session.commit()

    return session_schema.jsonify(new_session)

# Get Users
@app.route('/user', methods=['GET'])
def get_users():
    # Require Authorization header
    try:
        access_token = request.headers['Authorization']
    except:
        return Response(status=401)
    session = Session.query.filter_by(access_token=access_token).first()
    # Return 401 if accesss token does not belong to an admin account
    if session.user.admin == False:
        return Response(status=401)

    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

# Get User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Get Me
@app.route('/user/me', methods=['GET'])
def get_me():
    try:
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
        session = Session.query.filter_by(access_token=access_token).first()
    except:
        return Response(status=400)
    
    if session.access_expiration > time.time():
        if user_agent == session.agent:
            return user_schema.jsonify(session.user)
    return Response(status=401)

# Update User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
        session = Session.query.filter_by(access_token=access_token).first()
    except:
        return Response(status=400)
    # Return 401 if the key does not belong to either the user or an admin account
    if (session.user.id != user.id and session.user.admin == False):
        return Response(status=401)
    
    # Check for updated keys. If no update is passed, use current information
    try:
        email = request.json['email']
    except KeyError:
        email = user.email
    try:
        password = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
    except KeyError:
        password = user.password
    try:
        username = request.json['username']
    except KeyError:
        username = user.username

    # Set the New Information
    user.email = email
    user.password = password
    user.username = username
    
    # Check token authentication before committing changes
    if session.access_expiration > time.time():
        if user_agent == session.agent and user.username == session.user_id:
            db.session.commit()
        elif session.user.admin:
            db.session.commit()
        return user_schema.jsonify(user)
    else: 
        return Response(status=401)


# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
        session = db.one_or_404(db.select(Session).filter_by(access_token=access_token))
    except:
        return Response(status=400)
    
    # Return 401 if the key does not belong to either the user or an admin account
    if (session.user.id != user.id and session.user.admin == False):
        return Response(status=401)
    # Return 401 if the Access token is expired
    if (time.time() > session.access_expiration):
        return Response(status=401)
    # Return 401 and purge the session if User-Agent differs from the one registered
    if (session.agent != user_agent):
        db.session.delete(session)
        db.session.commit()
        return Response(status=401)
    
    # Delete all user sessions
    for session in user.auth:
        db.session.delete(session)
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

## Auth

# Login
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        hashedPass = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
        agent = request.headers['User-Agent']
        user = User.query.filter_by(username=username).first()
    except:
        return Response(status=400)
    if type(user) == NoneType:
        return Response(status=404)
    
    # Check Password
    if hashedPass == user.password:
        ## If the current user agent matches an existing session, use that session
        for session in user.auth:
            if session.agent == agent:
                session.generateTokens()
                db.session.commit()
                return session_schema.jsonify(session)
        
        # Otherwise, generate a new session
        newSession = Session(agent)
        newSession.user = user
        
        db.session.commit()
        return session_schema.jsonify(newSession)
    else:
        return Response(status=401)
            
# Refresh
@app.route('/auth/refresh', methods=['GET'])
def refresh():
    try:
        refreshToken = request.headers['Authorization']
        agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    userSession = db.one_or_404(db.select(Session).filter_by(refresh_token=refreshToken))
    
    # Check to see if the refresh token has expired
    if time.time() < userSession.refresh_expiration:
        userSession.generateTokens()
        db.session.commit()
        
        # If the requesting agent matches the session agent, return session information
        if userSession.agent == agent:
            return session_schema.jsonify(userSession)
        
        # If the requesting agent does not match the session agent, delete the session to require the agent to log in again.
        else: 
            db.session.delete(userSession)
            db.session.commit()
    else:
        return Response(status=401, mimetype='application/json', content_type='application/json')

# Check
@app.route('/auth/check', methods=['GET'])
def check_auth():
    try:
        accessToken = request.headers['Authorization']
        agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    userSession = db.one_or_404(db.select(Session).filter_by(access_token=accessToken))
    expiration = userSession.access_expiration
    loginStatus = False
    
    # If the user agent does not match, delete the session
    if userSession.agent != agent:
        db.session.delete(userSession)
        db.session.commit()
    
    # Check Access Token Expiration and verify login status if valid
    if time.time() < expiration:
        loginStatus = True

    return jsonify({"auth":loginStatus, "exp":expiration or None})

def createDefaultAdminAccount():
    email = 'admin@example.com'
    password = 'dbAdmin'
    username = 'admin'
    hashedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    adminUser = User(username=username, password=hashedPass, email=email, admin=True)
    db.session.add(adminUser)
    db.session.commit()

# Run Server
if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # createDefaultAdminAccount()
        app.run(debug=True)