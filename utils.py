from app import db, bcrypt, app
from app.models import User

db.drop_all()
db.create_all()

hashed_password = bcrypt.generate_password_hash('111').decode('utf-8')
a = User(username = "Joe", email = "xd@gmail.com", password=hashed_password, region="India")
db.session.add(a)

db.session.commit()