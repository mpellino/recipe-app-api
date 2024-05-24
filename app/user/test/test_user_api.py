"""
Test for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create') #get the url from the view to create the user
TOKEN_URL = reverse('user:token') #get the url from the view to create the token

def create_user(**params):
    """Create and return an new user."""
    return get_user_model().objects.create_user(**params)


class pubblicUserApiTest(TestCase):
    """Test the public feature of the API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is succesfull."""
        payload = {
            'email': 'test@example.com',
            'password': '123pass',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_with_email_exist_error(self):
        """test error returned if user with email exist:
        the create_user function is called first to create a user. 
        Then, a POST request is made to the API with the same payload, 
        trying to create a user with the same email. 
        This is done to test the API's behavior when trying to create a 
        user with an email that already exists in the database. 
        The test checks if the API correctly returns a 400 BAD REQUEST 
        status code in this scenario."""

        payload = {
            'email': 'test@example.com',
            'password': '123pass',
            'name': 'Test Name',
        }

        create_user(**payload) 

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        """Test an error is return if password is less than 5 chars."""

        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)


    def test_token_is_created_succesfully(self):
        """Test a token is generate"""

        user_details = {
            'email':'test@example.com',
            'password': 'test-token-pass123',
            'name': 'Test name'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
       

    def test_create_token_bad_credential(self):
        """Test returns error if invalid creadentials"""

        user_details = {
            'email':'test@example.com',
            'password': 'test-token-pass123',
            'name': 'Test name'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': 'wrong_password'
        }

        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_token_blank_password(self):
        """Test returns error if blank password"""

        payload = {
            'email': 'user@example.com',
            'password': ''
        }

        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)