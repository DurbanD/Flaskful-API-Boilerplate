from init import db, app
from Models.Session import Session
import time
from flask import request, Response

@app.route('/auth/logout', methods=['POST'])
def logout():
    # Get Required Headers
    try:
        accessToken = request.headers['Authorization']
    except:
        return Response(status=400)
    
    # Check for valid session
    userSession = db.one_or_404(db.select(Session).filter_by(access_token=accessToken))
    
    # Check Session expiration
    if (time.time() > userSession.access_expiration):
        return Response(status=400)
    db.session.delete(userSession)
    db.session.commit()
    return Response(status=200)
    