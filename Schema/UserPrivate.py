from init import ma
from Schema.Session import SessionSchema

sessions_schema = SessionSchema(many=True)
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'admin', 'auth')
    auth = ma.Nested(sessions_schema)

user_schema_private = UserSchema()
users_schema_private = UserSchema(many=True)