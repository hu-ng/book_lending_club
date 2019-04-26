import unittest
import requests

def log_in(self, email, password):
    return requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data=dict(email=email, password=password))


class FlaskTestCase(unittest.TestCase):
    
    #Ensuring that the default user is able to log in by asserting that the status code for this request is 200
    def test_correct_login(self):
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
    """    
    
    def test_login_required_userpage(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/user/1')
        self.assertNotIn('Borrowed Books', response.text)
        
    def test_login_required_notification(self):
        response = requests.get('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/notification')
        self.assertNotIn('Requests sent', response.text) 
        
    #Test whether users are able to add books
    def test_user_add_book(self):
        log_in(self, "xd@gmail.com", "111")
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/add_books', data=dict(bookname="test book", author="test author", numpages=123, condition="used"))
        self.assertTrue(response.status_code == 200) 
        
        
if __name__ == '__main__':
    unittest.main()
    
