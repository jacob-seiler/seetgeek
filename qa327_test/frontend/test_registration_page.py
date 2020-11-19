import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend homepage.

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
    # No account with these creds exists
    @patch('qa327.backend.get_user', return_value=None)
    # Register went ok
    @patch('qa327.backend.register_user', return_value=None)
    # Register with working info, check that you get redirected to /login
    def test_registration_success(self, *_):
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
        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text("User exists", "#message")

    # Learn how to do session info changes
    def test_registration_logged_in(self, *_):
        pass

    def test_registration_email_badformat(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@whoops")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text("Email format invalid.", "#message")

    def test_registration_name_nonalpha(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Ca$h Man")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text(
            "Name must only contain alphanumeric characters or spaces.", "#message")

    def test_registration_name_trailing(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", " bruh ")
        self.type("#password", "Password123")
        self.type("#password2", "Password123")

        self.click('input[type="submit"]')

        self.assert_text(
            "First and last characters can't be spaces.", "#message")

    def test_registration_password_noupper(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "password")
        self.type("#password2", "password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one uppercase character.", "#message")

    def test_registration_password_nolower(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "PASSWORD")
        self.type("#password2", "PASSWORD")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one lowercase character.", "#message")

    def test_registration_password_nospecial(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password")
        self.type("#password2", "Password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one special character.", "#message")

    def test_registration_password2_nomatch(self, *_):
        self.open(base_url + '/register')

        self.type("#email", "tester0@gmail.com")
        self.type("#name", "Tester Zero")
        self.type("#password", "Password123")
        self.type("#password2", "Password124")

        self.click('input[type="submit"]')

        self.assert_text("The passwords do not match", "#message")


class FrontEndHomePageTest(BaseCase):

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
