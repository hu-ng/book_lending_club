from flask import render_template, request, url_for, flash, redirect
from app import app, bcrypt, db
from .forms import RegistrationForm, LoginForm, AddBookForm, RequestForm
from .models import User, Meta_book, Book,Transaction
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date

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
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        region=form.region.data)
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


# add books
@app.route('/add_books', methods=["GET", "POST"])
@login_required
def add_books():
    form = AddBookForm()
    if form.validate_on_submit():
        meta_book = Meta_book.query.filter_by(name=form.bookname.data,
                                              author=form.author.data).first()
        # if meta book exist, we add the copy
        if meta_book:
            copy = Book(metabook_id=meta_book.id,
                        owner_id=current_user.id,
                        condition=form.condition.data,
                        region=current_user.region)
            db.session.add(copy)
            db.session.commit()
        # If meta book doesn't exist, we need to add the meta book first
        else:
            meta = Meta_book(name=form.bookname.data,
                             author=form.author.data,
                             numpages=form.numpages.data)
            db.session.add(meta)
            db.session.commit()
            meta_book = Meta_book.query.filter_by(name=form.bookname.data,
                                                  author=form.author.data).first()
            copy = Book(metabook_id=meta_book.id,
                        owner_id=current_user.id,
                        condition=form.condition.data,
                        region=current_user.region)
            db.session.add(copy)
            db.session.commit()
        flash(f'Sucessfully added the book {form.bookname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('test_add_book.html', title="Add Book", form=form)

# book display page
@app.route('/book_display')
@login_required
def book_display():
    books = Book.query.all()
    book_names = []
    for book in books:
        name = Meta_book.query.filter_by(id=book.metabook_id).first().name
        book_names.append(name)
    book_items = zip(books, book_names)
    return render_template('display.html', books=book_items)


@app.route('/borrowing_request/<int:book_id>',methods=["GET", "POST"])
@login_required
def borrowing_request(book_id):
    form = RequestForm()
    if form.validate_on_submit():
        if (form.start_date.data > form.end_date.data) or (form.start_date.data < date.today()):
            flash(f'Invalid Date!', 'danger')
            return redirect(url_for('index'))
        else:
            transaction = Transaction(book_id=book_id,
                                      borrower_id=current_user.id,
                                      startdate=form.start_date.data,
                                      enddate=form.end_date.data)
            db.session.add(transaction)
            db.session.commit()
            flash(f'Sucessfully requested the book!', 'success')
            return redirect(url_for('index'))
    return render_template("test_request_book.html",title="Request", form=form)


@app.route('/notification_page',methods=['GET','POST'])
@login_required
def notification_page():
    # Sent requests
    sent_requests = Transaction.query.filter_by(borrower_id=current_user.id,status='open').all()
    sent_book_names = []
    for s in sent_requests:
        metabook_id = Book.query.filter_by(id=s.book_id).first().metabook_id
        name = Meta_book.query.filter_by(id=metabook_id).first().name
        sent_book_names.append(name)
    request_items = zip(sent_requests,sent_book_names)

    # Received requests
    book_own_id = Book.query.filter_by(owner_id=current_user.id).all()
    received_requests = Transaction.query.filter_by(book_id=book_own_id,status='open').all()
    received_book_names = []
    borrower_names = []
    start_date = []
    end_date = []
    for r in received_requests:
         metabook_id = Book.query.filter_by(id=r.book_id).first().metabook_id
         book_name = Meta_book.query.filter_by(id=metabook_id).first().name
         received_book_names.append(book_name)
         borrower_name = User.query.filter_by(id=r.borrower_id).first().username
         borrower_names.append(borrower_name)
         start_date.append(r.startdate)
         end_date.append(r.enddate)
    received_items = zip(received_requests,received_book_names,borrower_names,start_date,end_date)


@app.route('/notification_page/<int:borrower_id>/<int:book_id>/lender_confirm', methods=["POST"])
@login_required
def lender_confirm(book_id, borrower_id):
    # Check to see if the current_user is the owner of the book_id
    owner_id = Book.query.filter_by(id=book_id).first().owner_id
    if owner_id == current_user.id:
        transaction = Transaction.query.filter_by(book_id=book_id, borrower_id=borrower_id).first()
        transaction.status = 'lender_confirmed'
        db.session.commit()
        flash(f'Successfully confirmed lending request!', 'success')
        return render_template('notification_page')
    flash(f"You don't have the right privileges to do this action", "danger")
    return render_template('notification_page')


@app.route("/notification_page/<int:borrower_id>/<int:book_id>/borrower_confirm", methods=["POST"])
@login_required
def borrower_confirm(book_id, borrower_id):
    if current_user.id == borrower_id:
        transaction = Transaction.query.filter_by(book_id=book_id, borrower_id=current_user.id).first()
        transaction.status = 'borrower_confirmed'
        db.session.commit()
        return redirect(url_for('notification_page'))
    flash(f"You don't have the right privileges to do this action", "danger")
    return redirect(url_for('notification_page'))


@app.route("/notification_page/<int:borrower_id>/<int:book_id>/return_confirm", methods=["POST"])
@login_required
def return_confirm(book_id, borrower_id):
    owner_id = Book.query.filter_by(id=book_id).first().owner_id
    if current_user.id == owner_id:
        transaction = Transaction.query.filter_by(book_id=book_id, borrower_id=borrower_id).first()
        transaction.status = 'return_confirmed'
        db.session.commit()
        return redirect(url_for('notification_page'))
        # Again, it's better to redirect the owner to the borrowing page, but with new info
    flash(f"You don't have the right privileges to do this action", "danger")
    return redirect(url_for('notification_page'))
