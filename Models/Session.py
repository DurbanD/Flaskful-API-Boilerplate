from init import db
import time
import secrets

# Session Model
class Session(db.Model):
    __tablename__="session"
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))
    user = db.relationship("User", back_populates="auth", uselist=False)
    
    agent = db.Column(db.String)
    issued = db.Column(db.Float)
    access_token = db.Column(db.String, unique = True)
    access_expiration = db.Column(db.Float)
    refresh_token = db.Column(db.String, unique = True)
    refresh_expiration = db.Column(db.Float)
    temp = db.Column(db.Boolean)
    refreshInterval = db.Column(db.Integer)
    accessInterval = db.Column(db.Integer)
    
    # 2592000 seconds is 30 days
    # 300 seconds is 5 minutes
    
    def __init__(self, agent, refreshExpires = 2592000, accessExpires = 300, temp=False ):
        self.agent = agent
        self.refreshInterval = refreshExpires
        self.accessInterval = accessExpires
        self.temp = temp
        self.refreshInterval = refreshExpires
        self.generateTokens()
    def generateTokens(self):
        issued = time.time()
        accessToken = secrets.token_hex(256)
        access_exp = time.time() + self.accessInterval
        
        # Do not allow refresh if temp
        if self.temp == False:
            refresh_exp = time.time() + self.refreshInterval
            refreshToken = secrets.token_hex(256)
        elif self.temp == True:
            refresh_exp = 0
            refreshToken = None
        
        # Set Column Values
        self.issued = issued
        self.access_token  = accessToken
        self.access_expiration = access_exp
        self.refresh_token = refreshToken
        self.refresh_expiration = refresh_exp