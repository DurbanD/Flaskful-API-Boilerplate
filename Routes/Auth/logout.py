from init import db, app
from Models.Session import Session
import time
from flask import request, jsonify, Response

@app.route('/auth/logout', methods=['POST'])
def logout():
    try:
        accessToken = request.headers['Authorization']
        agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    userSession = db.one_or_404(db.select(Session).filter_by(access_token=accessToken))
    expiration = userSession.access_expiration
    if (time.time() > expiration):
        return Response(status=400)
    db.session.delete(userSession)
    db.session.commit()
    return Response(status=200)
    