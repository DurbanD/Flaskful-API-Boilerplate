from init import db, app
from Schema.init import session_schema
from Models.Session import Session
from Models.User import User
import hashlib
from flask import request, jsonify, Response
from Tools.emailValidator import validate

@app.route('/user', methods=['POST'])
def post_user():
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