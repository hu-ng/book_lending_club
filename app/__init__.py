from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'a8c24e8ea6fb2993715e4c3a4aa8996d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['database_username'], os.environ['database_pwd'], os.environ['database_host'], os.environ['database_db'])
db = SQLAlchemy(app)
# set up login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

# bcrypt for password
bcrypt = Bcrypt()

from app import routes
