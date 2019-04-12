from app import db, bcrypt, app
from app.models import User, Meta_book, Book

db.drop_all()
db.create_all()

hashed_password = bcrypt.generate_password_hash('111').decode('utf-8')
a = User(username = "Joe", email = "xd@gmail.com", password=hashed_password, region="sf")
db.session.add(a)

db.session.commit()

# add book
meta = Meta_book(name="Book_Meta", author="Mr. XD", numpages="8787")
db.session.add(meta)
db.session.commit()

book = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta", author="Mr. XD").first().id,
			owner_id=User.query.filter_by(username = "Joe", email = "xd@gmail.com").first().id, 
            condition="new", region="sf")
