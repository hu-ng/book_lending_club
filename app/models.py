from app import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, nullable = False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String, nullable = False)
	#Should actually find these checking the books table.
	#books = db.Column()
	#lent = db.Column()
	#stars = db.Column(db.Integer)
	
	# def __init__(self, username, password, stars):
	# 	self.username = username
	# 	self.password = password
	# 	#Should actually find these checking the books table.
	# 	#self.books = books
	# 	#self.lent = lent
	# 	stars = stars
	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"