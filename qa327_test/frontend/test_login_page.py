import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the login page.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""

# Moch a sample user
test_user = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password=generate_password_hash('Password123')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):
    def test_default_not_logged_in(self, *_):
        """
        If the user hasn't logged in, show the login page.
        """
        # Log out user
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page contains #login-title
        self.assert_element("#login-title")
    
    def test_default_logged_in(self, *_):
        """
        If the user has logged in, do not show the login page.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Log in user using #email and #password
        self.open(base_url + '/login')
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        self.click('input[type="submit"]')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page does not contain #login-header
        self.assert_element_not_present("#login-title")
    
    def test_login_message_exists(self, *_):
        """
        The login page has a message.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page contains #message
        self.assert_element("#message")
    
    def test_login_message_default(self, *_):
        """
        The login page has a message that by default says 'Please login'.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that #message contains value "Please login"
        self.assert_text("Please login", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')

        # after clicking on the browser (the line above)
        # the front-end code is activated
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics.
        # so we patch the backend to return a specific user instance,
        # rather than running that program. (see @ annotations above)

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Hi Tester Zero !", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password124")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("email/password combination incorrect", "#message")
