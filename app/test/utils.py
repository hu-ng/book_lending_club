from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

# db = SQLAlchemy(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/pepeflores/Documents/cs162-book-lending/test/data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['database_username'], os.environ['database_pwd'], os.environ['database_host'], os.environ['database_db'])

db = SQLAlchemy(app)

class User(db.Model):

	__tablename__ = "Users"
	
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, nullable = False)
	password = db.Column(db.String, nullable = False)
	#Should actually find these checking the books table.
	#books = db.Column()
	#lent = db.Column()
	stars = db.Column(db.Integer)
	
	def __init__(self, username, password, stars):
		self.username = username
		self.password = password
		#Should actually find these checking the books table.
		#self.books = books
		#self.lent = lent
		stars = stars

#class Meta_book(db.Model):
#
#	__tablename__ = "Metabooks"
#
#	id = db.Column()
#	name = db.Column(db.String(), nullable = False)
#	author = db.Column(db.String(), nullable =False)
#	numpages = db.Column(db.Integer, nullable = False)
#
#
#class Book(db.Model):
#
#	__tablename__ = "Books"
#
#	metabook = db.Column()
#	availability = db.Column(db.Boolean, nullable = False)
#	owner_id = db.Column(db.Integer, nullable =False)
#	condition = db.Column(db.Boolean, nullable = False)
#
#
#class Transactions(db.Model):
#
#	__tablename__ = "Transactions"
#
#	book_id = db.Column(db.Integer)
#	# We could get the lender_id using book_id
#	lender_id = db.Column(db.Integer)
#	borrower_id = db.Column()
#	status = db.Column()




a = User("Joe", "xd", 4)
db.session.add(a)

b = User("John", "lol", 3)
db.session.add(b)

c = User("Mike", "takitaki", 2)
db.session.add(c)
db.session.commit()