import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User
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
    email='tester1@gmail.com',
    name='Tester One',
    password='Password123',
    balance=5000
)

test_user_exists = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password='Password123'
)


class FrontEndRegistrationPageTest(BaseCase):
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_registration_logged_in(self, *_):
        """
        If the user has logged in, redirect back to the user profile page /
        Test case ID: R2.1.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')

        # Log in using `#username` and `#password`
        self.open(base_url + '/login')
        self.type("#email", test_user_exists.email)
        self.type("#password", test_user_exists.password)
        self.click('input[type="submit"]')

        # Open /register
        self.open(base_url + '/register')

        # Validate that current page does not contain `#title`
        self.assert_element_absent("#title")

    @patch('qa327.backend.get_user', return_value=None)
    def test_registration_not_logged_in(self, *_):
        """
        If the user has not logged in, show the user registration page
        Test case ID: R2.1.2
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')

        # Open /register
        self.open(base_url + '/register')

        # Validate that current page includes `#title`
        self.assert_element_present("#title")

    def test_registration_form_present(self, *_):
        """
        The registration page shows a registration form requesting: email, user name, password, password2
        The registration page shows a registration form requesting the field email
        The registration page shows a registration form requesting the field user name
        The registration page shows a registration form requesting the field password
        The registration page shows a registration form requesting the field password2
        Test case ID: R2.2.1, R2.2.2, R2.2.3, R2.2.4, R2.2.5
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')

        # Open /register
        self.open(base_url + '/register')

        # Validate `#form` is displayed
        self.assert_element_present("#register-form")
        self.assert_element_present("#email")
        self.assert_element_present("#name")
        self.assert_element_present("#password")
        self.assert_element_present("#password2")

    @patch('qa327.backend.register_user', return_value=False)
    def test_email_empty(self, *_):
        """
        Email is not empty - negative
        Test case ID: R2.4.2
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", "")
        self.type("#name", test_user.name)
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        # Check that we did not leave the register page
        self.assert_element_present("#title")

    @patch('qa327.backend.register_user', return_value=False)
    def test_password_empty(self, *_):
        """
        Password is not empty - negative
        Test case ID: R2.4.3
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "")
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        # Check that we did not leave the register page
        self.assert_element_present("#title")

    @patch('qa327.backend.register_user', return_value=False)
    def test_password2_empty(self, *_):
        """
        Password2 is not empty - negative
        Test case ID: R2.4.4
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", test_user.password)
        self.type("#password2", "")

        self.click('input[type="submit"]')

        # Check that we did not leave the register page
        self.assert_element_present("#title")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_email_badformat(self, *_):
        """
        Email follows addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation) - positive
        Test case ID: R2.5.2
        """

        self.open(base_url + '/register')

        self.type("#email", "tester0@whoops")
        self.type("#name", test_user.name)
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        self.assert_text("Email format invalid.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_password_min(self, *_):
        """
        Password is at least 6 characters - negative
        Test case ID: R2.6.2
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "abcde")
        self.type("#password2", "abcde")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must be at least 6 characters long.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_password_noupper(self, *_):
        """
        Password contains at least one upper case - negative
        Test case ID: R2.6.3
        """
        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "password")
        self.type("#password2", "password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one uppercase character.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_password_nolower(self, *_):
        """
        Password contains at least one lower case - negative
        Test case ID: R2.6.4
        """

        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "PASSWORD")
        self.type("#password2", "PASSWORD")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one lowercase character.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_password_nospecial(self, *_):
        """
        Password contains at least one special character - negative
        Test case ID: R2.6.5
        """
        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "Password")
        self.type("#password2", "Password")

        self.click('input[type="submit"]')

        self.assert_text(
            "Password must have at least one special character.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_password2_nomatch(self, *_):
        """
        Password and Password2 are exactly the same - negative
        Test case ID: R2.7.2
        """
        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", "Password123")
        self.type("#password2", "Password124")

        self.click('input[type="submit"]')

        self.assert_text("The passwords do not match", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_name_nonalpha(self, *_):
        """
        User name is alphanumeric-only - negative
        Test case ID: R2.8.2
        """
        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", "Ca$h Man")
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        self.assert_text(
            "Name must only contain alphanumeric characters or spaces.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_name_trailing(self, *_):
        """
        User name contains space that is not the first or the last character - negative
        Test case ID: R2.8.3
        """
        self.open(base_url + '/register')

        self.type("#email", test_user.email)
        self.type("#name", " bruh ")
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        self.assert_text(
            "First and last characters can't be spaces.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_username_too_short(self, *_):
        """
        User name is longer than 2 characters - negative
        Test case ID: R2.9.2
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", "ab")
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        self.assert_text(
            "Name must be longer than 2 characters.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_username_too_long(self, *_):
        """
        User name is shorter than 20 characters - negative
        Test case ID: R2.9.3
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", "abcdefghijklmnopqrst")
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        self.assert_text(
            "Name must be shorter than 20 characters.", "#message")

    @patch('qa327.backend.register_user', return_value=False)
    def test_registration_userexists(self, *_):
        """
        If the email already exists, show message 'this email has been ALREADY used'
        Test case ID: R2.10
        """
        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user_exists.email)
        self.type("#name", test_user_exists.name)
        self.type("#password", test_user_exists.password)
        self.type("#password2", test_user_exists.password)

        self.click('input[type="submit"]')

        self.assert_text("User exists", "#message")

    @patch('qa327.backend.register_user', return_value=True)
    def test_registration_success(self, *_):
        """
        The registration form can be submitted as a POST request to the current URL (/register)
        Email, password and password2 are not empty - positive
        Email follows addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation) - positive
        Password meets the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character - positive
        Password and Password2 are exactly the same - positive
        User name has to be non-empty, alphanumeric-only, and space allowed only if it is not the first or the last character - positive
        User name has to be longer than 2 characters and less than 20 characters - positive
        If all inputs are correct, create a new user, set the balance to 5000, and go back to the /login page
        Test case IDs: R2.3, R2.4.1, R2.5.1, R2.6.1, R2.7.1, R2.8.1, R2.9.1, R2.11
        """
        self.open(base_url + '/logout')

        self.open(base_url + '/register')

        self.assert_text("Register", "#title")

        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)

        self.click('input[type="submit"]')

        # Ensure POST request has been sent
        self.assert_text("Please login", "#message")
