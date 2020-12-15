import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the logout page.

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


class FrontEndLogoutPageTest(BaseCase):
    def test_logout_invalidates(self, *_):
        """
        Logout will invalidate the current session and redirect to the login page.
        Test case ID: R7.1.1
        """
        # Log in user using #email and #password
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")
        # Open /logout
        self.open(base_url + "/logout")
        # Validate that current page contains #login-title
        self.assert_element("#login-title")

    def test_logout_restricts(self, *_):
        """
        After logout, the user shouldn't be able to access restricted pages.
        Test case ID: R7.1.2
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + "/logout")
        # Open /
        self.open(base_url)
        # Validate that current page contains #login-title
        self.assert_element("#login-title")
