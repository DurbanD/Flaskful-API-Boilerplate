from init import db, app
from Schema.init import user_schema
from Models.Session import Session
from Models.User import User
import time
from flask import request, jsonify, Response

# Get Me
@app.route('/user/me', methods=['GET'])
def get_me():
    try:
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    session = db.one_or_404(db.select(Session).filter_by(access_token=access_token))
    
    if session.access_expiration > time.time():
        if user_agent == session.agent:
            return user_schema.jsonify(session.user)
    return Response(status=401)