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
    
    def test_redirect_logged_in(self, *_):
        """
        If the user has logged in, redirect to the user profile page.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Log in user using #email
        self.open(base_url + '/login')
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        self.click('input[type="submit"]')
        # Open /
        self.open(base_url)
        # Validate that current page contains #welcome-header
        self.assert_element("#welcome-header")
    
    def test_redirect_not_logged_in(self, *_):
        """
        If the user hasn't logged in, don't redirect to the user profile page
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /
        self.open(base_url)
        # Validate that current page doesn't contain #welcome-header
        self.assert_element_not_present("#welcome-header")
    
    def test_login_form(self, *_):
        """
        The login page provides a login form.
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #login-form is displayed
        self.assert_element("#login-form")

    def test_login_form_email(self, *_):
        """
        The login page provides a login form which requests the field email.
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #email is displayed
        self.assert_element("#email")

    def test_login_form_password(self, *_):
        """
        The login page provides a login form which requests the field password.
        """
        # Open /login
        self.open(base_url + '/login')
        # Validate #password is displayed
        self.assert_element("#password")
    
    def test_login_form_submit_post(self, *_):
        """
        The login form can be submitted as a POST request to the current URL (/login).
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into #email
        self.type("#email", "tester0@gmail.com")
        # Enter value into #password
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate POST request sent to current URL (/login)
        self.open(base_url)
        self.assert_element("#welcome-header")

    def test_email_password_not_empty(self, *_):
        """
        Email and password are not empty.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is not empty
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible("email/password format is incorrect.", "#message")

    def test_email_empty(self, *_):
        """
        Email is empty.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is empty
        self.type("#email", "")
        # Enter value into form field #password that is not empty
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_empty(self, *_):
        """
        Password is empty.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is empty
        self.type("#password", "")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_email_valid(self, *_):
        """
        Email follows addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation).
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that follows addr-spec defined in RFC 5322
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible("email/password format is incorrect.", "#message")

    def test_email_invalid(self, *_):
        """
        Email doesn't follow addr-spec defined in RFC 5322 (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation).
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that doesn't follow addr-spec defined in RFC 5322
        self.type("#email", "tester0gmail.com")
        # Enter value into form field #password
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_small(self, *_):
        """
        Password does not meet the required complexity since length is less than 6.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is less than 6 characters long
        self.type("#password", "hello")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")
    
    def test_password_uppercase(self, *_):
        """
        Password does not meet the required complexity since no uppercase.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that has no uppercase characters
        self.type("#password", "thishasnouppercase")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_lowercase(self, *_):
        """
        Password does not meet the required complexity since no lowercase.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that has no lowercase characters
        self.type("#password", "THISHASNOLOWERCASE")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_special(self, *_):
        """
        Password does not meet the required complexity since no special character.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that has no special characters
        self.type("#password", "thisHasNoSpecialCharacters")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_complex(self, *_):
        """
        Password meets the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not empty
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is at least than 6 characters long, contains at least one upper case character, at least one lower case character, and at least one special character
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible("email/password format is incorrect.", "#message")

    def test_email_formatting_errors(self, *_):
        """
        For any email formatting errors, render the login page and show the message 'email/password format is incorrect.'.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email with formatting error(s)
        self.type("#email", "tester0gmail.com")
        # Enter value into form field #password without formatting error(s)
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_password_formatting_errors(self, *_):
        """
        For any password formatting errors, render the login page and show the message 'email/password format is incorrect.'.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email without formatting error(s)
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password with formatting error(s)
        self.type("#password", "password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password format is incorrect.", "#message")

    def test_no_formatting_errors(self, *_):
        """
        If no formatting errors, don't show the message 'email/password format is incorrect.'.
        """
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email without formatting error(s)
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password withoutformatting error(s)
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible("email/password format is incorrect.", "#message")

    def test_redirect(self, *_):
        """
        If email/password are correct, redirect to /
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is correct
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #welcome-header is displayed
        self.assert_element("#welcome-header")

    def test_password_correct(self, *_):
        """
        If email isn't correct, redict to /login and show message 'email/password combination incorrect'.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is not correct
        self.type("#email", "wrongemail@gmail.com")
        # Enter value into form field #password that is correct
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password combination incorrect", "#message")

    def test_email_correct(self, *_):
        """
        If password isn't correct, redict to /login and show message 'email/password combination incorrect'.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is not correct
        self.type("#password", "wrongPassword123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message displays error
        self.assert_text("email/password combination incorrect", "#message")

    def test_email_and_password_correct(self, *_):
        """
        If email/password are correct, don't show message 'email/password combination incorrect'.
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /login
        self.open(base_url + '/login')
        # Enter value into form field #email that is correct
        self.type("#email", "tester0@gmail.com")
        # Enter value into form field #password that is correct
        self.type("#password", "Password123")
        # Click #btn-submit
        self.click("#btn-submit")
        # Validate #message does not display error
        self.assert_text_not_visible("email/password combination incorrect", "#message")

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
