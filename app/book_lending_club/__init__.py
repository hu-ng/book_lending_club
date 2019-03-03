from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['database_username'], os.environ['database_pwd'], os.environ['database_host'], os.environ['database_db'])
db = SQLAlchemy(app)

from book_lending_club import routes
