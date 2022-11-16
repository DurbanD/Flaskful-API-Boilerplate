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

    # If the username is an email, get user by email. Else get by usernme.
    if validate(username) == True:
        user = db.one_or_404(db.select(User).filter_by(email=username))
    else:
        user = db.one_or_404(db.select(User).filter_by(username=username))

    # Look through the user's auth sessions, delete anything expired, and return unauthorized if a valid temporary token already exists. 
    for session in user.auth:
        if time.time() >= session.access_expiration:
            db.session.delete(session)
            db.session.commit()
            continue
        if session.temp == False:
            continue
        if session.temp == True:
            return Response(status=401)

    # Generate a temp token
    tempToken = Session(agent, accessExpires=1800, temp=True)
    tempToken.user = user
    db.session.commit()
    
    #Email the temp token to be used by the guest to change their password via PUT to /User/<id>
    user_email = user.email
    send(user_email, tempToken)
    
    # This return should be removed in production and is only for debugging. User should only get their recovery token in a URL sent in an email.
    return session_schema.jsonify(tempToken)