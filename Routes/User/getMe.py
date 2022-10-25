from init import db, app
from Schema.UserPrivate import user_schema_private
from Models.Session import Session
import time
from flask import request, Response

# Get Me
@app.route('/user/me', methods=['GET'])
def get_me():
    try:
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    session = db.one_or_404(db.select(Session).filter_by(access_token=access_token))
    
    # Send 401 if access token is temp
    if session.temp == True:
        return Response(status=401)
    
    if session.access_expiration > time.time():
        if user_agent == session.agent:
            return user_schema_private.jsonify(session.user)
    return Response(status=401)