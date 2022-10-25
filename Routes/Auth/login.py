from init import db, app
from Schema.Session import session_schema
from Models.Session import Session
from Models.User import User
import hashlib
from flask import request, Response
from Tools.emailValidator import validate

# Login
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        hashedPass = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
        agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    if validate(username) == True:
        user = db.one_or_404(db.select(User).filter_by(email=username))
    else:
        user = db.one_or_404(db.select(User).filter_by(username=username))
    
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