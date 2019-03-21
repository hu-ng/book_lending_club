from app import db, app, login_manager
from models import User


a = User("Joe", "xd", 4)
db.session.add(a)

b = User("John", "lol", 3)
db.session.add(b)

c = User("Mike", "taki", 2)
db.session.add(c)
db.session.commit()