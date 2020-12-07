from sys import base_exec_prefix
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


class BackEndUpdateTest(BaseCase):
    def test_ticket_is_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", "t1")
        self.type("#update-form-quantity", "50")
        self.type("#update-form-price", "70")
        self.type("#update-form-expiration-date", "99990117")
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Successfully updated ticket'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_is_not_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", "hello $$$")
        self.type("#update-form-quantity", "50")
        self.type("#update-form-price", "70")
        self.type("#update-form-expiration-date", "99990117")
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Invalid ticket. Could not update.", "#flash-message")
