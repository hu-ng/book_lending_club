from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.check_img_url import is_url_image

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'a8c24e8ea6fb2993715e4c3a4aa8996d'

# from environment variables
db_username = os.environ['database_username']
db_pwd = os.environ['database_pwd']
db_host = os.environ['database_host']
db = os.environ['database_db']


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(db_username, db_pwd, db_host, db)
db = SQLAlchemy(app)
# set up login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"

# bcrypt for password
bcrypt = Bcrypt()

# add check url image function
app.jinja_env.globals.update(is_url_image=is_url_image)



from app import routes
