from init import db, app
from Models.Session import Session
import time
from flask import request, jsonify, Response

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