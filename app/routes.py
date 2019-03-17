from flask import render_template, request
from app import app
from .forms import RegistrationForm
from .models import User

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

# Register page
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if request.method=="POST" and form.validate():
        # Validate username and email
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not user and not email:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created", "success")
            return redirect(url_for('login'))
        # Username has already been taken
        else:
            flash("Username or email has already been taken", "error")
            return render_template("register.html", title="Register", form=form)
    return render_template("register.html", title="Register", form=form)
