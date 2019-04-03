from app import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(40), nullable = False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable = False)
	
	books = db.relationship('Book', backref='user', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"



class Meta_book(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(40), nullable = False)
	author = db.Column(db.String(40), nullable =False)
	numpages = db.Column(db.Integer, nullable = False)
	
	copies = db.relationship('Book', backref='metas', lazy=True)

	def __repr__(self):
		return f"Meta_book('{self.name}', '{self.author}')"


class Book(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	
	metabook_id = db.Column(db.Integer, db.ForeignKey('meta_book.id'), nullable=False)
	
	owner_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	availability = db.Column(db.Boolean, nullable = False)
	condition = db.Column(db.Boolean, nullable = False)

	def __repr__(self):
		return f"Book('{self.name}', '{self.author}')"