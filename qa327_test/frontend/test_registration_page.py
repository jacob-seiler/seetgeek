import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the register page.

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


class FrontEndRegistrationPageTest(BaseCase):
    @patch('qa327.backend.get_user', return_value=None)
    @patch('qa327.backend.register_user', return_value=None)
    def test_registration_success(self, *_):
        """
        Test to make sure if all checks are passed, the user is able to create a 
        valid new account. Mocking is done to verify no user with that info exists,
        and the new user was able to be created. 
        """
        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text("Please login", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_registration_userexists(self, *_):
        """
        Test to check if user already exists. Patching required to return existing
        user.
        """
        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text("User exists", "#message")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_registration_logged_in(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')

        # open home page
        self.open(base_url + '/register')
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Hi Tester Zero !", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    # Check that a bad email format returns an error
    def test_registration_email_badformat(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@whoops")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text("Email format invalid.", "#message")

    # Check that a name with non-alphanumeric chars gives error
    def test_registration_name_nonalpha(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Ca$h Man")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text(
            "Name must only contain alphanumeric characters or spaces.", "#message")

    # Check that a name with trailing spaces gives error
    def test_registration_name_trailing(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", " bruh ")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text(
            "First and last characters can't be spaces.", "#message")

    # Check that a password with no uppercase chars gives error
    def test_registration_password_noupper(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "password")
        self.type("#password2", "password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one uppercase character.", "#message")

    # Check that a password with no lowercase chars gives error
    def test_registration_password_nolower(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "PASSWORD")
        self.type("#password2", "PASSWORD")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one lowercase character.", "#message")

    # Check that a password with no special chars gives error
    def test_registration_password_nospecial(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password")
        self.type("#password2", "Password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one special character.", "#message")

    # Check that a nonmatching password2 gives error
    def test_registration_password2_nomatch(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password124")

        self.click('input[type="submit"]')

        self.assert_text("The passwords do not match", "#message")
