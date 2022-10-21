from types import NoneType
from init import db, app
from Schema.init import session_schema
from Models.Session import Session
from Models.User import User
import hashlib
from flask import request, jsonify, Response

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