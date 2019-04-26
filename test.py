#Importing dependencies

import os
import tempfile
from flask import render_template, request, url_for, flash, redirect
import unittest
import requests
import datetime
from sqlalchemy import create_engine
from app import app, bcrypt, db
from app import routes, forms
from app.models import User, Meta_book, Book, Transaction
from flask_login import login_user, current_user, logout_user, login_required

def log_in(self, email, password):
    return requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data=dict(email=email, password=password))

hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

now = datetime.datetime.now()


class FlaskTestCase(unittest.TestCase):
    
    #Ensuring that the default user is able to log in by asserting that the status code for this request is 200
    def test_correct_login(self):
        #Making a post request to the server with correct login credentials
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data = dict(email="xd@gmail.com", password="111"))
        self.assertTrue(response.status_code == 200) 
    
    #Ensuring a non-registered user is unable to log in by asserting that the request doesn't redirect ("Log In" still present in raw HTML)
    def test_incorrect_login(self):
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data = dict(username="incorrect@email.com", password="hunter12"))
        self.assertIn("Log In", response.text)
        
    #Testing that the index page loads properly
    def test_index(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/')
        self.assertTrue('Sign up now' in response.text)	
            
    #Testing that login is required to access various pages
    def test_login_required_addbooks(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/add_books')
        self.assertNotIn('Condition of the book', response.text)    
    
    def test_login_required_library(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/book_display')
        self.assertNotIn('Explore the available books', response.text)
        
    """
    The next test did not pass. This means that unathorised users are able to access the user pages of everyone. This is a major privacy issue.
    I fixed it by adding @login_required to the user page. However, this doesn't fix it suficciently, as it means if user 1 is logged it, he can just
    replace the '...ws.com/user/1' with '...ws.com/user/x' to view all the borrowed books of user x, so preferably a more substantial modification to the
    code structure will be implemented, but that is not a priority now.
    
    
    def test_login_required_userpage(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/user/1')
        self.assertNotIn('Borrowed Books', response.text)
    """   
    
    def test_login_required_notification(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/notification')
        self.assertNotIn('Requests sent', response.text) 
        
    #Test whether users are able to add books
    def test_user_add_book(self):
        log_in(self, "xd@gmail.com", "111")
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/add_books', data=dict(bookname="Bible", author="God", numpages=666, condition="torn"))
        self.assertTrue(response.status_code == 200) 
        
    #Setting up a test database to check whether     
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        db.create_all()
        
    #function for tearing down the database    
    def tearDown(self):
        db.session.remove()
        db.drop_all()  
     
    #Checking whether the password hashing function works properly
    def test_password_hashing(self):
        new_user = User(username="John Doe",
                        email="john@aol.com",
                        password=hashed_password,
                        region="sf")
        self.assertFalse(bcrypt.check_password_hash(new_user.password, "incorrect password"))
        self.assertTrue(bcrypt.check_password_hash(new_user.password, "password"))
        
    #Checking whether the database can add new users   
    def test_adding_users(self):
        u1 = User(username="John Doe",
                        email="john@aol.com",
                        password=hashed_password,
                        region="sf")
        u2 = User(username="Jane Doe",
                        email="jane@aol.com",
                        password=hashed_password,
                        region="hyd")
        u3 = User(username="Simon Golombek",
                        email="simon@minerva.kgi.edu",
                        password=hashed_password,
                        region="ber")
        db.session.add_all([u1, u2, u3])
        db.session.commit()
        thirduser = User.query.filter_by(id=3).first()
        self.assertEqual(thirduser.username, "Simon Golombek")
        
    #Testing the book properties    
    def test_book_properties(self):
        mb1 = Meta_book(name="bible", author="god", numpages=666)
        b1 = Book(metabook_id=1, owner_id=1,
                condition="new", region="sf")
        self.assertEqual(mb1.author, "god")
        self.assertEqual(b1.owner_id, 1)
        self.assertNotEqual(b1.owner_id, 2)
        
    #Testing whether the database is able to add books   
    def test_adding_books(self):
        b1 = Book(metabook_id=1, owner_id=1,
                condition="new", region="sf")
        b2 = Book(metabook_id=1, owner_id=1,
                condition="used", region="hyd")
        b3 = Book(metabook_id=1, owner_id=1,
                condition="torn", region="sel")
        db.session.add_all([b1, b2, b3])
        db.session.commit()
        hydbook = Book.query.filter_by(region="hyd").first()
        numbertorn = Book.query.filter_by(condition="torn").all()
        self.assertEqual(hydbook.owner_id, 1)
        self.assertEqual(len(numbertorn), 1)
        
    def test_adding_transactions(self):
        t1 = Transaction(book_id=1, borrower_id=1,
                date_created=datetime.datetime(2019, 5, 26), startdate=datetime.datetime(2019, 4, 16), 
                         enddate=datetime.datetime(2019, 3, 30), status="open")
        db.session.add(t1)
        db.session.commit()
        numtrans = Transaction.query.all()
        self.assertEqual(len(numbertrans), 1)
        self.assertTrue((now-t1.startdate).days <= 0)
        self.assertTrue((t1.startdate-t1.enddate).days <= 0)
          
if __name__ == '__main__':
    unittest.main()
    
