from Schema.Session import SessionSchema
from Schema.User import UserSchema

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)