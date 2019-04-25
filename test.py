import app
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class IntegrationTest(unittest.TestCase):
    def test_loginsuccess(self):
        r = requests.post('http://localhost:5000/login', data= {'username': "Username", 'password': "12345", 'confirm_password': "12345"})
        self.assertEqual(r.status_code,200)


if __name__ == '__main__':
    unittest.main()
