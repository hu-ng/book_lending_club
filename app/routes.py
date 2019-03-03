from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['database_username'], os.environ['database_pwd'], os.environ['database_host'], os.environ['database_db'])
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

# Page for all books available 
@app.route('/book_store')
def book_store():
    return render_template('bookstore.html')

# User profile page
@app.route('/<int:id>/profile')
def user_profile(id):
    return render_template('profile.html', id=user_id)

# Book show page
@app.route('/book/<int:id>')
def book(id):
    return render_template('book.html', id=book_id)

# Book lending request page
@app.route('/transaction/<int:lender_id>/<int:borrower_id>')
def transaction(lender_id, borrower_id):
    return render_template('transaction.html', lender=lender_id, borrower_id=borrower_id)

if __name__ == '__main__':
    app.run(debug=True)
