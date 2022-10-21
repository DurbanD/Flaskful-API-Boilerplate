from init import ma

class SessionSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'access_token', 'access_expiration', 'refresh_token', 'refresh_expiration')