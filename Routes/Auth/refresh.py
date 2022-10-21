from init import db, app
from Schema.init import session_schema
from Models.Session import Session
from Models.User import User
import time
from flask import request, Response

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