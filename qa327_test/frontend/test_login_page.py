import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User
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
    password='Password123',
    balance=5000
)


class FrontEndLoginPageTest(BaseCase):
    def test_default_logged_in(self, *_):
        """
        If the user has logged in, do not show the login page
        Test case ID: R1.1.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Log in user using #email and #password
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page does not contain #login-title
        self.assert_element_absent("#login-title")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_default_not_logged_in(self, *_):
        """
        If the user hasn't logged in, show the login page
        Test case ID: R1.1.2
        """
        # Log out user
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page contains #login-title
        self.assert_element("#login-title")

    def test_login_message_exists(self, *_):
        """
        The login page has a message
        Test case ID: R1.2.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that current page contains #message
        self.assert_element("#message")

    def test_login_message_default(self, *_):
        """
        The login page has a message that by default says 'Please login'
        Test case ID: R1.2.2
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Validate that #message contains value "Please login"
        self.assert_text("Please login", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_redirect_logged_in(self, *_):
        """
        If the user has logged in, redirect to the user profile page
        Test case ID: R1.3.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Log in user using #email
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Open /
        self.open(base_url)
        # Validate that current page contains #welcome-header
        self.assert_element("#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_redirect_not_logged_in(self, *_):
        """
        If the user hasn't logged in, don't redirect to the user profile page
        Test case ID: R1.3.2
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /
        self.open(base_url)
        # Validate that current page doesn't contain #welcome-header
        self.assert_element_absent("#welcome-header")

    def test_login_form(self, *_):
        """
        The login page provides a login form
        Test case ID: R1.4.1
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #login-form is displayed
        self.assert_element("#login-form")

    def test_login_form_email(self, *_):
        """
        The login page provides a login form which requests the field email
        Test case ID: R1.4.2
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #email is displayed
        self.assert_element("#email")

    def test_login_form_password(self, *_):
        """
        The login page provides a login form which requests the field password
        Test case ID: R1.4.3
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #password is displayed
        self.assert_element("#password")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_login_form_submit_post(self, *_):
        """
        The login form can be submitted as a POST request to the current URL (/login)
        Test case ID: R1.5
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into #email
        self.type("#email", test_user.email)
        # Enter value into #password
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate POST request sent to current URL (/login)
        self.open(base_url)
        self.assert_element("#welcome-header")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_email_password_not_empty(self, *_):
        """
        Email and password are not empty
        Test case ID: R1.6.1
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that is not empty
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible(
            "email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_email_empty(self, *_):
        """
        Email is empty
        Test case ID: R1.6.2
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is empty
        self.type("#email", "")
        # Enter value into form field #password that is not empty
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_empty(self, *_):
        """
        Password is empty
        Test case ID: R1.6.3
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that is empty
        self.type("#password", "")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_email_valid(self, *_):
        """
        Email follows addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation) - positive
        Test case ID: R1.7.1
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that follows addr-spec defined in RFC 5322
        self.type("#email", test_user.email)
        # Enter value into form field #password
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible(
            "email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_email_invalid(self, *_):
        """
        Email follows addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation) - negative
        Test case ID: R1.7.2
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that doesn't follow addr-spec defined in RFC 5322
        self.type("#email", "tester0gmail.com")
        # Enter value into form field #password
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_small(self, *_):
        """
        Password does not meet the required complexity since length is less than 6
        Test case ID: R1.8.1
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that is less than 6 characters long
        self.type("#password", "hello")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_uppercase(self, *_):
        """
        Password does not meet the required complexity since no uppercase
        Test case ID: R1.8.2
        """
        # Logout to invalidate current session
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that has no uppercase characters
        self.type("#password", "thishasnouppercase")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_lowercase(self, *_):
        """
        Password does not meet the required complexity since no lowercase
        Test case ID: R1.8.3
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that has no lowercase characters
        self.type("#password", "THISHASNOLOWERCASE")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_special(self, *_):
        """
        Password does not meet the required complexity since no special character
        Test case ID: R1.8.4
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that has no special characters
        self.type("#password", "thisHasNoSpecialCharacters")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_password_complex(self, *_):
        """
        Password meets the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character
        Test case ID: R1.8.5
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", test_user.email)
        # Enter value into form field #password that is at least than 6 characters long, contains at least one upper case character, at least one lower case character, and at least one special character
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible(
            "email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_email_formatting_errors(self, *_):
        """
        For any email formatting errors, render the login page and show the message 'email/password format is incorrect.'
        Test case ID: R1.9.1
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email with formatting error(s)
        self.type("#email", "tester0gmail.com")
        # Enter value into form field #password without formatting error(s)
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_formatting_errors(self, *_):
        """
        For any password formatting errors, render the login page and show the message 'email/password format is incorrect.'
        Test case ID: R1.9.2
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email without formatting error(s)
        self.type("#email", test_user.email)
        # Enter value into form field #password with formatting error(s)
        self.type("#password", '$')
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_no_formatting_errors(self, *_):
        """
        If no formatting errors, don't show the message 'email/password format is incorrect.'
        Test case ID: R1.9.3
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email without formatting error(s)
        self.type("#email", test_user.email)
        # Enter value into form field #password withoutformatting error(s)
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible(
            "email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_redirect(self, *_):
        """
        If email/password are correct, redirect to /
        Test case ID: R1.10
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", test_user.email)
        # Enter value into form field #password that is correct
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #welcome-header is displayed
        self.assert_element("#welcome-header")

    @patch('qa327.backend.login_user', return_value=None)
    def test_password_correct(self, *_):
        """
        If email isn't correct, redict to /login and show message 'email/password combination incorrect'
        Test case ID: R1.11.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not correct
        self.type("#email", "wrongemail@gmail.com")
        # Enter value into form field #password that is correct
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password combination incorrect", "#message")

    @patch('qa327.backend.login_user', return_value=None)
    def test_email_correct(self, *_):
        """
        If password isn't correct, redict to /login and show message 'email/password combination incorrect'
        Test case ID: R1.11.2
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", test_user.email)
        # Enter value into form field #password that is not correct
        self.type("#password", "wrongtest_user.password")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    @patch('qa327.backend.login_user', return_value=test_user)
    def test_email_and_password_correct(self, *_):
        """
        If email/password are correct, don't show message 'email/password combination incorrect'
        Test case ID: R1.11.3
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", test_user.email)
        # Enter value into form field #password that is correct
        self.type("#password", test_user.password)
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible(
            "email/password combination incorrect", "#message")
