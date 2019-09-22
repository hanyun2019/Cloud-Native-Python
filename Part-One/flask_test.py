# Test cases for restful API
# Haowen Huang modified on Sep 22, 2019
# Implementation of Cloud Native web applications
# Part One: Developing a RESTful micro service in Python 
#
# Test cases for RESTful API:
# $ nosetests
# 

from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_users_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/v1/users')
        print (result)
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_tweets_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/v2/tweets')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_addusers_status_code(self):
        # sends HTTP POST request to the application
        # on the specified path
        result = self.app.post('/api/v1/users', data='{ "username":"Ovestint", "email": "ronaldrvera@jourrapide.com", "password": "juzahpei6e", "name":"Ronald R. Vera"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEquals(result.status_code, 201)

    def test_updusers_status_code(self):
        # sends HTTP PUT request to the application
        # on the specified path
        # User case: Ovestint|ronaldrvera@jourrapide.com|juzahpei6e|Ronald R. Vera|17
        #
        result = self.app.put('/api/v1/users/17', data='{"username":"Tagning", "emailid": "leolaLguertin@teleworm.us"}', content_type='application/json')
        # assert the status code of the response
        self.assertEquals(result.status_code, 200)

    def test_addtweets_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        # User case: Tagning|leolaLguertin@teleworm.us|juzahpei6e|Ronald R. Vera|17
        #
        result = self.app.post('/api/v2/tweets', data='{"username":"Tagning", "body": "It Works!#Awesome"}', content_type='application/json')

        # assert the status code of the response
        self.assertEqual(result.status_code, 201)

    def test_delusers_status_code(self):
        # sends HTTP Delete request to the application
        # on the specified path
        # User case: Tagning|leolaLguertin@teleworm.us|juzahpei6e|Ronald R. Vera|17
        #
        result = self.app.delete('/api/v1/users', data='{"username":"Tagning"}', content_type='application/json')
        print (result)
        # assert the status code of the response
        self.assertEquals(result.status_code, 200)
