from types import NoneType
from init import app
from Models.Session import Session
from Models.User import User
from Schema.UserPrivate import user_schema_private
from Schema.UserPublic import user_schema_public
from flask import request
import time

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    try:
        access_token = request.headers['Authorization']
        user_agent = request.headers['User-Agent']
    except:
        return user_schema_public.jsonify(user)
    userSession = Session.query.filter_by(access_token=access_token).first()
    # Return public information if no user session is found
    if type(userSession) == NoneType:
        return user_schema_public.jsonify(user)
    # Return public if user session is expired
    if userSession.access_expiration < time.time():
        return user_schema_public.jsonify(user)
    # Return public if user agent differs
    if userSession.agent != user_agent:
        return user_schema_public.jsonify(user)
    # Return private if the request comes from the user or an admin account
    if userSession.user.id == user.id or userSession.user.admin == True:
        return user_schema_private.jsonify(user)
    # Return public otherwise
    return user_schema_public.jsonify(user)