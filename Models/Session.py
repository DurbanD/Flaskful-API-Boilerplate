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
    
    def __init__(self, agent):
        self.generateTokens()
        self.agent = agent
    def generateTokens(self):
        issued = time.time()
        sessionToken = secrets.token_hex(256)
        refreshToken = secrets.token_hex(256)
        
        session_exp = time.time() + 300
        # 300 seconds is 5 minutes
        refresh_exp = time.time() + 259200
        # 2592000 seconds is 30 days
        
        self.issued = issued
        self.access_token  = sessionToken
        self.access_expiration = session_exp
        self.refresh_token = refreshToken
        self.refresh_expiration = refresh_exp