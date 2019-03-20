from flask import render_template, request, url_for, flash, redirect
from app import app, bcrypt, db
from .forms import RegistrationForm, LoginForm
from .models import User
from flask_login import login_user, current_user, logout_user


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
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # We do not have such method for User model: new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created", "success")
        return redirect(url_for('login'))
    # Template for registration would be test_register.html for now
    return render_template("test_register.html", title="Register", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Log In Successful', 'success')
            # After successful log in, redirects to main page, wherever that is.
            return redirect(url_for('index'))
        else:
            flash('Log In Failed. Please recheck credentials', 'danger')
    return render_template('test_login.html', title='Log In', form=form)


@app.route('/logout', methods=["GET","POST"])
def logout():
    logout_user()
    # Returns the user to the home page
    return redirect(url_for('index'))
