from init import db, app
from Models.User import User
from Models.Session import Session
from Schema.Session import session_schema
import time
from flask import request, Response
from Tools.emailValidator import validate
from Tools.RecoveryEmailer import send

@app.route('/auth/recover', methods=['POST'])
def recover_auth():
    try:
        username = request.json['username']
        agent = request.headers['User-Agent']
    except:
        return Response(status=400)
    
    if validate(username) == True:
        user = db.one_or_404(db.select(User).filter_by(email=username))
    else:
        user = db.one_or_404(db.select(User).filter_by(username=username))
    for session in user.auth:
        if time.time() >= session.access_expiration:
            db.session.delete(session)
            db.session.commit()
            continue
        if session.temp == False:
            continue
        if session.temp == True:
            return Response(status=401)

    tempToken = Session(agent, accessExpires=1800, temp=True)
    tempToken.user = user
    db.session.commit()
    
    user_email = user.email
    send(user_email, tempToken)
    
    return session_schema.jsonify(tempToken)