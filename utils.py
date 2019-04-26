from app import db, bcrypt, app
from app.models import User, Meta_book, Book

db.drop_all()
db.create_all()

hashed_password = bcrypt.generate_password_hash('111').decode('utf-8')
a = User(username = "Joe", email = "xd@gmail.com", password=hashed_password, region="sf")
u1 = User(username = "Jane", email = "jn@gmail.com", password=hashed_password, region="ba")
u2 = User(username = "Hana", email = "hn@gmail.com", password=hashed_password, region="ln")
u3 = User(username = "Joe123", email = "jd@gmail.com", password=hashed_password, region="hd")
u4 = User(username = "Maria", email = "maria@gmail.com", password=hashed_password, region="sf")
db.session.add(a)
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)

db.session.commit()

# add book
meta = Meta_book(name="Book_Meta", author="Mr. XD", numpages="8787")
m1 = Meta_book(name="Book_Meta1", author="Mr. XD1", numpages="87")
m2 = Meta_book(name="Book_Meta2", author="Mr. XD2", numpages="287")
m3 = Meta_book(name="Book_Meta3", author="Mr. XD3", numpages="587")
m4 = Meta_book(name="Book_Meta4", author="Mr. XD4", numpages="135")
db.session.add(meta)
db.session.add(m1)
db.session.add(m2)
db.session.add(m3)
db.session.add(m4)
db.session.commit()

book = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta", author="Mr. XD").first().id,
			owner_id=User.query.filter_by(username = "Joe", email = "xd@gmail.com").first().id, 
            condition="new", region="sf")
book1 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta1", author="Mr. XD1").first().id,
			owner_id=User.query.filter_by(username = "Joe123", email = "jd@gmail.com").first().id, 
            condition="used", region="hd")
book2 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta2", author="Mr. XD2").first().id,
			owner_id=User.query.filter_by(username = "Joe", email = "xd@gmail.com").first().id, 
            condition="new", region="sf")
book3 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta3", author="Mr. XD3").first().id,
			owner_id=User.query.filter_by(username = "Maria", email = "maria@gmail.com").first().id, 
            condition="new", region="sf")
book4 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta4", author="Mr. XD4").first().id,
			owner_id=User.query.filter_by(username = "Maria", email = "maria@gmail.com").first().id, 
            condition="used", region="sf")
book5 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta1", author="Mr. XD1").first().id,
			owner_id=User.query.filter_by(username = "Joe", email = "xd@gmail.com").first().id, 
            condition="new", region="sf")
book6 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta2", author="Mr. XD2").first().id,
			owner_id=User.query.filter_by(username = "Hana", email = "hn@gmail.com").first().id, 
            condition="new", region="ln")
book7 = Book(metabook_id=Meta_book.query.filter_by(name="Book_Meta3", author="Mr. XD3").first().id,
			owner_id=User.query.filter_by(username = "Jane", email = "jn@gmail.com").first().id, 
            condition="used", region="ba")

db.session.add(book)
db.session.add(book1)
db.session.add(book2)
db.session.add(book3)
db.session.add(book4)
db.session.add(book5)
db.session.add(book6)
db.session.add(book7)
db.session.commit()
