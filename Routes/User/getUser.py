from init import db, app
from Schema.init import user_schema
from Models.Session import Session
from Models.User import User

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)