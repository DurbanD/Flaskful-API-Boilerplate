from init import ma

# /User/<id> Endpoint Result for non-owner and non-admin requests
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')
user_schema_public = UserSchema()
users_schema_public = UserSchema(many=True)