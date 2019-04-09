from app import db, app, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    region = db.Column(db.String(60), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"



class Meta_book(db.Model):
    __tablename__ = 'meta_book'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable = False)
    author = db.Column(db.String(40), nullable =False)
    numpages = db.Column(db.Integer, nullable = False)
    
    copies = db.relationship('Book', backref='metas', lazy=True)

    def __repr__(self):
        return f"Meta_book('{self.name}', '{self.author}')"


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key = True)
    metabook_id = db.Column(db.Integer, db.ForeignKey('meta_book.id'), nullable=False) 
    owner_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    region = db.Column(db.String(60), nullable=False)
    availability = db.Column(db.Boolean, nullable = False, default=True)
    condition = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"Book('{self.name}', '{self.author}')"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key = True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    date_created = db.Column(db.DateTime, nullable=False, server_default=func.now() )
    
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String(60), nullable = False, default = "open")

    def __repr__(self):
        return f"Transaction('{self.book_id}', '{self.borrower_id}', '{self.lender_id}')"

