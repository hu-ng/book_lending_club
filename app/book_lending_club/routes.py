from flask import render_template
from book_lending_club import app


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

