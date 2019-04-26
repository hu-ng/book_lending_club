import unittest
import requests

class FlaskTestCase(unittest.TestCase):
    
    #Ensuring that the default user is able to log in by asserting that the status code for this request is 200
    def test_correct_login(self):
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data = dict(email="xd@gmail.com", password="111"))
        self.assertTrue(response.status_code == 200) 
     
    #Ensuring a non-registered user is unable to log in by asserting that the request doesn't redirect ("Log In" still present in raw HTML)
    def test_incorrect_login(self):
        response = requests.post('http://ec2-18-219-248-53.us-east-2.compute.amazonaws.com/login', data = dict(email="incorrect@email.com", password="hunter12"))
        self.assertIn(b"Log In", response.text)  

if __name__ == '__main__':
    unittest.main()
