from init import app
from Schema.UserPrivate import users_schema_private
from Models.Session import Session
from Models.User import User
from flask import request, jsonify, Response
import time

@app.route('/user', methods=['GET'])
def get_users():
    # Require Authorization header
    try:
        access_token = request.headers['Authorization']
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', default=5, type=int)
    except:
        return Response(status=401)
    
    # Set minimum and maximum limit and offset values
    if limit > 100:
        limit = 100
    if offset < 0:
        offset = 0    
    
    # Return 401 if accesss token is expired or does not belong to an admin account
    session = Session.query.filter_by(access_token = access_token).first()
    if session.user.admin == False or time.time() > session.access_expiration:
        return Response(status=401)
    # Send 401 if access token is temp
    if session.temp == True:
        return Response(status=401)

    # Package the data
    users = User.query.all()
    result = users_schema_private.dump(users[ offset: offset + limit ])
    data = {
        "total": len(users),
        "offset": offset,
        "limit": limit,
        "result": result
    }
    
    return jsonify(data)