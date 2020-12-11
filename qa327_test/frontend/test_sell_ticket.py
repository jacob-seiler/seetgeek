import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket


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
    password='Password123'
)

# Mock a sample ticket
test_ticket = Ticket(
    name='tickot',
    quantity=50,
    price=50.00,
    expiration_date='20771210'
)


class FrontEndHomePageTest(BaseCase):

    # Test that with valid values there are no errors present
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.create_ticket', return_value=None)
    @patch('qa327.backend.get_all_tickets', return_value=[])
    def test_ticket_sell_post_success(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', test_ticket.name)
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', test_ticket.quantity)
        # Enter value into form_sell_price
        self.type('#sell-form-price', test_ticket.price)
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_element_absent('#flash-message')

    # Test that with invalid name there is error present
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.create_ticket', return_value=None)
    @patch('qa327.backend.get_all_tickets', return_value=[])
    def test_ticket_sell_post_name_error(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', "$$$ HOTLINE - BLING $$$")
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', test_ticket.quantity)
        # Enter value into form_sell_price
        self.type('#sell-form-price', test_ticket.price)
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_text(
            "Name must have alphanumeric characters only.", '#flash-message')

    # Test that with invalid quantity there is error present
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.create_ticket', return_value=None)
    @patch('qa327.backend.get_all_tickets', return_value=[])
    def test_ticket_sell_post_quantity_error(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', test_ticket.name)
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', 0)
        # Enter value into form_sell_price
        self.type('#sell-form-price', test_ticket.price)
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_text(
            "Quantity must be between 1 and 100.", '#flash-message')

    # Test that with invalid price there is error present
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.create_ticket', return_value=None)
    @patch('qa327.backend.get_all_tickets', return_value=[])
    def test_ticket_sell_post_price_error(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', test_ticket.name)
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', test_ticket.quantity)
        # Enter value into form_sell_price
        self.type('#sell-form-price', 0)
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_text(
            "Price must be between 10 and 100 inclusive.", '#flash-message')

    # Test that with invalid date there is error present

    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.create_ticket', return_value=None)
    @patch('qa327.backend.get_all_tickets', return_value=[])
    def test_ticket_sell_post_date_error(self, *_):
        """
        The ticket-selling form can be posted to /sell
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_sell_name
        self.type('#sell-form-name', test_ticket.name)
        # Enter value into form_sell_quantity
        self.type('#sell-form-quantity', test_ticket.quantity)
        # Enter value into form_sell_price
        self.type('#sell-form-price', test_ticket.price)
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', 2000)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_text(
            "Date must be in the format YYYYMMDD.", '#flash-message')
