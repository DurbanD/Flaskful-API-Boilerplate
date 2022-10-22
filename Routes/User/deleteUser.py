from init import db, app
from Schema.UserPublic import user_schema_public
from Models.Session import Session
from Models.User import User
import time
from flask import request, Response

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
        session = db.one_or_404(db.select(Session).filter_by(access_token=access_token))
    except:
        return Response(status=400)
    
    # Return 401 if the key does not belong to either the user or an admin account
    if (session.user.id != user.id and session.user.admin == False):
        return Response(status=401)
    # Return 401 if the Access token is expired
    if (time.time() > session.access_expiration):
        return Response(status=401)
    # Return 401 and purge the session if User-Agent differs from the one registered
    if (session.agent != user_agent):
        db.session.delete(session)
        db.session.commit()
        return Response(status=401)
    
    # Delete all user sessions
    for session in user.auth:
        db.session.delete(session)
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    return user_schema_public.jsonify(user)