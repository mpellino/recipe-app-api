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
ME_URL = reverse ('user:me')

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

    def test_authentication_required(self):
        """Test return anauthorized access if user is not logged in"""

        res = self.client.get(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    class PrivateUserApiTest(TestCase):
        """Test API requests that required authenticated users"""

        def setUp(self):
            """method for creating a user"""

            user_details = {
                'email':'test@example.com',
                'password': 'test-token-pass123',
                'name':'Test_name'
                }

            self.user = create_user(**user_details)
            self.client = APIClient()
            self.client.force_authenticate(self.user)

        def test_retreive_profile_sucess(self):
            """Test retreiving profile for logged user success"""

            res = self.client.get(ME_URL)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data, {
                'name':self.user.name,
                'email':self.user.email
            })

        def post_request_not_allow(self):
            """TEst post request is not allow for ME_API"""

            res = self.client.post(ME_URL)
            self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_update_user_profile(self):
            """Test the API updates the user details"""

            updated_user_details = {
                'name':'updatred_name',
                'password':'updated_password'
            }

            res = self.client.patch(ME_URL, updated_user_details)

            self.user.refresh_from_db()

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(self.user.name, updated_user_details['name'])
            self.assertTrue(self.user.check_password(updated_user_details['password']))
