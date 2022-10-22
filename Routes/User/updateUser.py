from init import db, app
from Schema.UserPrivate import user_schema_private
from Models.Session import Session
from Models.User import User
import hashlib
import time
from flask import request, jsonify, Response
from Tools.emailValidator import validate

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
        return user_schema_private.jsonify(user)
    else: 
        return Response(status=401)