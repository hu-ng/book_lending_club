from flask import render_template, request, url_for, flash, redirect
from sqlalchemy import and_
from app import app, bcrypt, db
from .forms import RegistrationForm, LoginForm, AddBookForm, RequestForm
from .models import User, Meta_book, Book, Transaction
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
from app.send_emails import send_email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete_book/<int:id>')
def delete_book(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()
    return render_template('deleted.html')

@app.route('/book/<int:id>')
def book_profile(id):
    book = Book.query.filter_by(id=id).first()
    metabook_id = book.metabook_id
    metabook = Meta_book.query.filter_by(id=metabook_id).first()
    name = metabook.name
    author = metabook.author
    numpages = metabook.numpages
    return render_template('book.html', book=book, metabook=metabook)

@app.route('/confirm_returned/<int:id>')
def confirm_returned(id):
    raise NotImplementedError

# User profile page
@app.route('/user/<int:id>')
@login_required
def user_profile(id):
    if id is None and current_user.is_authenticated:
        id=current_user.id
    elif id is None:
        return redirect(url_for('login'))

    user = User.query.filter_by(id=id).first()

    ownedQ = Book.query.filter_by(owner_id=id)
    borrowedQ = Transaction.query.filter_by(status='borrower_confirmed', borrower_id=id)

    owned = []
    borrowed = []

    for book in ownedQ:


        name = Meta_book.query.filter_by(id=book.metabook_id).first().name
        author = Meta_book.query.filter_by(id=book.metabook_id).first().author

        t = Transaction.query.filter_by(status='borrower_confirmed', book_id = book.id).first()
        if t:
            status = 'out'
            borrower = User.query.filter_by(id=t.borrower_id).first().username
        else:
            status = 'in'
            borrower = None


        owned.append((name,author,book.id,book.metabook_id,status,borrower))

    for t in borrowedQ:
        today = datetime.now()
        due = (t.enddate - datetime.now()).days

        book = Book.query.filter_by(id=t.book_id).first()

        name = Meta_book.query.filter_by(id=book.metabook_id).first().name
        author = Meta_book.query.filter_by(id=book.metabook_id).first().author
        owner = User.query.filter_by(id=book.owner_id).first().username
        ownerID = User.query.filter_by(id=book.owner_id).first().id

        borrowed.append((name,author,book.id,book.metabook_id,due,owner,ownerID))


    return render_template('profile.html', id=id, user=user, borrowed = borrowed, owned = owned)


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
    return render_template("register.html", title="Register", form=form)


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
    return render_template('login.html', title='Log In', form=form)


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
        meta_book = Meta_book.query.filter_by(name=form.bookname.data, author=form.author.data).first()
        # if meta book exist, we add the copy
        if meta_book:
            copy = Book(metabook_id=meta_book.id, owner_id=current_user.id,
                condition=form.condition.data, region=current_user.region,
                img=form.img.data)
            db.session.add(copy)
            db.session.commit()
        # If meta book doesn't exist, we need to add the meta book first
        else:
            meta = Meta_book(name=form.bookname.data, author=form.author.data,
                            numpages=form.numpages.data)
            db.session.add(meta)
            db.session.commit()
            meta_book = Meta_book.query.filter_by(name=form.bookname.data, author=form.author.data).first()
            copy = Book(metabook_id=meta_book.id, owner_id=current_user.id,
                condition=form.condition.data, region=current_user.region,
                img=form.img.data)
            db.session.add(copy)
            db.session.commit()
        flash(f'Sucessfully added the book {form.bookname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html', title="Add Book", form=form)

# book display page
@app.route('/book_display')
@login_required
def book_display():
    books = Book.query.all()
    metas = []
    for book in books:
        meta = Meta_book.query.filter_by(id=book.metabook_id).first()
        metas.append(meta)
    # we can just add in the meta book object and query specific items from the object
    book_items = zip(books, metas)
    return render_template('display.html', books=book_items)


@app.route('/borrowing_request/<int:book_id>', methods=["GET", "POST"])
@login_required
def borrowing_request(book_id):
    # A check to make sure book owners can't borrow their own books
    curr_book = Book.query.filter_by(id=book_id).first()
    if curr_book.owner_id == current_user.id:
        return redirect(url_for('book_display'))

    # Find the last transaction of the same book from the same user
    prev_transaction = Transaction.query.filter_by(book_id=book_id,
                                                   borrower_id=current_user.id)\
        .order_by(Transaction.id.desc()).first()

    form = RequestForm()

    # If there is no existing transaction for this user and for this book
    # If the last transaction is canceled or finished, then the current user can request again
    if prev_transaction is None or prev_transaction.status == 'canceled' \
            or prev_transaction.status == 'return_confirmed':
        if form.validate_on_submit():
            if (form.start_date.data < form.end_date.data) and (form.start_date.data > date.today()):
                transaction = Transaction(book_id=book_id,
                                          borrower_id=current_user.id,
                                          startdate=form.start_date.data,
                                          enddate=form.end_date.data)
                db.session.add(transaction)
                db.session.commit()
                # Notify the owner of the book.
                holder_id = Book.query.filter_by(id=book_id).first().owner_id
                holder_email = User.query.filter_by(id=holder_id).first().email
                send_email(receiver = holder_email,
                           topic = "requesting",
                           book_id = book_id)
                # Notify the user he successfully requested the book.
                send_email(receiver = current_user.email,
                           topic = "requested",
                           book_id = book_id)
                flash(f'Successfully requested the book!', 'success')
                return redirect(url_for('notification'))
            else:
                flash(f'Dates are not valid (make sure that start date is before the end date and after today)', 'danger')
                return redirect(url_for('borrowing_request', book_id = book_id))
        return render_template("test_request_book.html", title="Request", form=form)

    # If the transaction is still in any other state, then do not let the transaction go through
    else:
        flash(f'You can\'t borrow this book yet', 'danger')
        return render_template("test_request_book.html", title="Request", form=form)


@app.route('/notification', methods=['GET', 'POST'])
@login_required
def notification():
    # Sent requests
    sent_requests = Transaction.query.filter(and_(Transaction.borrower_id == current_user.id,
                                                  Transaction.status != "return_confirmed")).all()
    # status='open' Removed to test the flow
    sent_book_owners = []
    sent_book_names = []
    for s in sent_requests:
        metabook_id = Book.query.filter_by(id=s.book_id).first().metabook_id
        name = Meta_book.query.filter_by(id=metabook_id).first().name
        sent_book_names.append(name)
        owner_id = Book.query.filter_by(id=s.book_id).first().owner_id
        sent_book_owner = User.query.filter_by(id=owner_id).first().username
        sent_book_owners.append(sent_book_owner)
    sent_items = zip(sent_requests, sent_book_names, sent_book_owners)

    # Received requests
    book_own_id = Book.query.filter_by(owner_id=current_user.id).all()
    book_ids = []
    for book in book_own_id:
        book_ids.append(book.id)
    # received_requests = Transaction.query.filter(and_(Transaction.book_id.in_(book_ids), Transaction.status == 'open')).all()
    # Commented out to test the flow
    received_requests = Transaction.query.filter(
        and_(Transaction.book_id.in_(book_ids), Transaction.status != 'return_confirmed')).all()
    received_book_names = []
    borrower_names = []
    for r in received_requests:
         metabook_id = Book.query.filter_by(id=r.book_id).first().metabook_id
         book_name = Meta_book.query.filter_by(id=metabook_id).first().name
         received_book_names.append(book_name)
         borrower_name = User.query.filter_by(id=r.borrower_id).first().username
         borrower_names.append(borrower_name)
    received_items = zip(received_requests, received_book_names, borrower_names)

    return render_template('notification_page.html', requests_sent=sent_items, requests_received=received_items)


@app.route('/cancel_request/<int:request_id>/', methods=['GET', 'POST'])
@login_required
def cancel_request(request_id):
    request = Transaction.query.filter_by(id=request_id).first()
    # Change the status of the request
    # If it's still an open request, no need for confirmation
    if request.status == 'open':
        request.status = 'cancelled'
        db.session.commit()
        flash(f'Successfully cancel this request!', 'success')
        return redirect(url_for('notification'))
    # If the borrower want to cancelled a confirmed request
    # They need confirmation from the lender
    elif current_user.id == request.borrower_id:
        request.status = "pending cancel"
        db.session.commit()
        flash(f'Cancellation process has been initiated', 'success')
        return redirect(url_for('notification'))
    # If the lender accept the canceling request
    # Change the status of the request in our database
    else:
        request.status = 'cancelled'
        flash(f'Successfully cancel this request!', 'success')
        return redirect(url_for('notification'))

@app.route('/reject_request/<int:request_id>/',methods=['GET','POST'])
@login_required
def reject_request(request_id):
    request = Transaction.query.filter_by(id=request_id).first()
    # Change the status of the request
    request.status = 'rejected'
    db.session.commit()
    # Send email notifying both parties
    requester_email = User.query.filter_by(id=request.borrower_id).first().email
    send_email(receiver = requester_email,
               topic = "reject1",
               book_id = request.book_id)
    send_email(receiver = current_user.email,
               topic = "reject2",
               book_id = request.book_id)
    return redirect(url_for('notification'))


@app.route('/notification/<int:request_id>/lender_confirm', methods=['GET','POST'])
@login_required
def lender_confirm(request_id):
    # Check to see if the current_user is the owner of the book_id
    transaction = Transaction.query.filter_by(id=request_id).first()
    book = Book.query.filter_by(id=transaction.book_id).first()
    if current_user.id == book.owner_id:
        transaction.status = 'lender_confirmed'
        # Rejects every other transaction
        alt_transactions = Transaction.query.filter_by(status='open', book_id=transaction.book_id)
        for request in alt_transactions:
            request.status = 'rejected'
        db.session.commit()
        # Notify everyone after the commit
        # The lender
        send_email(receiver = current_user.email,
                   topic = "l_confirm2",
                   book_id = transaction.book_id)
        # The requester
        requester_email  = User.query.filter_by(id=transaction.borrower_id).first().email
        send_email(receiver = requester_email,
                   topic = "l_confirm1",
                   book_id = transaction.book_id)
        # The other requesters
        for request in alt_transactions:
            alt_req_email = User.query.filter_by(id=request.borrower_id).first().email
            send_email(receiver = alt_req_email,
                       topic = "reject1",
                       book_id = transaction.book_id)
            send_email(receiver = current_user.email,
                       topic = "reject2",
                       book_id = transaction.book_id)
        flash(f'Successfully confirmed lending request!', 'success')
        return redirect(url_for('notification'))
    flash(f"You don't have the right privileges to do this action", "danger")
    return redirect(url_for('notification'))


@app.route("/notification/<int:request_id>/borrower_confirm", methods=['GET','POST'])
@login_required
def borrower_confirm(request_id):
    transaction = Transaction.query.filter_by(id=request_id).first()
    if current_user.id == transaction.borrower_id:
        transaction.status = 'borrower_confirmed'
        db.session.commit()
        return redirect(url_for('notification'))
    flash(f"You don't have the right privileges to do this action", "danger")
    return redirect(url_for('notification'))


@app.route("/notification_page/<int:request_id>/return_confirm", methods=['GET','POST'])
@login_required
def return_confirm(request_id):
    transaction = Transaction.query.filter_by(id=request_id).first()
    book = Book.query.filter_by(id=transaction.book_id).first()
    if current_user.id == book.owner_id:
        transaction.status = 'return_confirmed'
        db.session.commit()
        return redirect(url_for('notification'))
    flash(f"You don't have the right privileges to do this action", "danger")
    return redirect(url_for('notification'))


@app.route("/notification/<int:request_id>/issue_raise", methods=['GET','POST'])
@login_required
def issue_raise(request_id):
    transaction = Transaction.query.filter_by(id=request_id).first()
    transaction.status = 'issue_raised'
    db.session.commit()
    return redirect(url_for('notification'))
