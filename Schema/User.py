from init import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'admin')