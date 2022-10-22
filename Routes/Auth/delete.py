from types import NoneType
from init import db, app
from Models.Session import Session
import time
from flask import request, Response

@app.route('/auth/<id>', methods=['DELETE'])
def delete_session(id):
    # Get Required Headers
    try:
        accessToken = request.headers['Authorization']
    except:
        return Response(status=400)
    
    # Check for valid session
    targetSession = Session.query.get(id)
    session = Session.query.filter_by(access_token=accessToken).first()
    if (type(targetSession) == NoneType or type(session) == NoneType):
        return Response(status=404)
    # session = db.one_or_404(db.select(Session).filter_by(access_token=accessToken))
    
    if targetSession.user.id != session.user.id and session.user.admin == False:
        return Response(status=401)
    
    # Check Session expiration
    if (time.time() > session.access_expiration):
        return Response(status=401)
    db.session.delete(targetSession)
    db.session.commit()
    return Response(status=200)
    