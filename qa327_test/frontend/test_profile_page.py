import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Ticket
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the profile page.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""

# Mock a sample user
test_user = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password=generate_password_hash('Password123')
)

# Mock some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):
    def test_not_logged_in_redirect(self, *_):
        #If the user is not logged in, redirect to login page

        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /
        self.open(base_url)
        # Validate that current page does not contain #profile_header
        self.assert_element_not_present('#profile_header')
    
    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_logged_in_load_profile(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that current page contains #profile_header
        self.assert_element
        ('#profile_header')

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_greeting_header(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that current page contains #profile_header
        self.assert_element('#welcome-header')

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_show_user_balance(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that current page contains #profile_header
        self.assert_element('#user-balance')

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_logout_link(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that page contains button #logout
        self.assert_element_present('#logout-link')

    def test_tickets(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that page contains element #tickets
        self.assert_element('#tickets')

    def test_ticket_sell_form(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that page contains element #sell-form
        self.assert_element('#sell-form')
        self.assert_element('#sell-form-name')
        self.assert_element('#sell-form-quantity')
        self.assert_element('#sell-form-price')
        self.assert_element('#sell-form-expiration-date')
    
    def test_ticket_buy_form(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that page contains element #buy-form
        self.assert_element('#buy-form')
        self.assert_element('#buy-form-name')
        self.assert_element('#buy-form-quantity')

    def test_ticket_update_form(self, *_):
        #If the user is logged in, load profile page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        # click enter button
        self.click('input[type="submit"]')
        # open / 
        self.open(base_url)
        # Validate that page contains element #update-form
        self.assert_element('#update-form')
        self.assert_element('#update-form-name')
        self.assert_element('#update-form-quantity')
        self.assert_element('#update-form-price')
        self.assert_element('#update-form-expiration-date')

    def test_ticket_sell_post(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", "tester0@gmail.com")
        self.type("#password", "Password123")
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', 'Ticket')
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', '1')
        # Enter value into form_sell_price
        self.type('#sell-form-price', '9.99')
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', '2020-11-20')
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_element('#sell-content')