from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DB
db = SQLAlchemy(app)

#Init Marshmallow
ma = Marshmallow(app)

# Get SSL Key Paths
# YOU MUST GENERATE A KEY AND A CERT TO USE THIS
# RUN Scripts/keygen.sh TO GENERATE THE KEY AND CERT
serverCert = os.path.join(basedir, 'server.crt')
serverKey = os.path.join(basedir, 'server.key')
