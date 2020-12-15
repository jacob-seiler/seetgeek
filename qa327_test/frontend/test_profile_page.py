import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket
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
    password='Password123',
    balance=5000
)

# Moch a sample ticket
test_ticket = Ticket(
    name='t1',
    quantity=50,
    price=70.50,
    expiration_date='20771210'
)


class FrontEndHomePageTest(BaseCase):
    def test_not_logged_in_redirect(self, *_):
        """
        If the user is not logged in, redirect to login page
        Test case ID: R3.1.1
        """
        # Log out user (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # Open /
        self.open(base_url)
        # Validate that current page does not contain #welcome-header
        self.assert_element_absent('#welcome-header')

    def test_logged_in_load_profile(self, *_):
        """
        If the user is logged in, load profile page
        Test case ID: R3.1.2
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that current page contains #welcome-header
        self.assert_element('#welcome-header')

    def test_greeting_header(self, *_):
        """
        This page shows a header 'Hi {}'.format(user.name)
        Test case ID: R3.2
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that current page contains ##welcome-header
        self.assert_element('#welcome-header')

    def test_show_user_balance(self, *_):
        """
        This page shows user balance
        Test case ID: R3.3
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that current page contains ##welcome-header
        self.assert_element('#user-balance')

    def test_logout_link(self, *_):
        """
        This page shows a logout link, pointing to /logout
        Test case ID: R3.4
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that page contains button #logout
        self.assert_element_present('#logout-link')

    def test_tickets(self, *_):
        """
        This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired.
        Test case ID: R3.5
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that page contains element #tickets
        self.assert_element('#tickets')

    def test_ticket_sell_form(self, *_):
        """
        This page contains a form that a user can submit new tickets for sell.
        This page contains a form that a user can submit new tickets for sell which requests the field name
        This page contains a form that a user can submit new tickets for sell which requests the field quantity
        This page contains a form that a user can submit new tickets for sell which requests the field price
        This page contains a form that a user can submit new tickets for sell which requests the field expiration date
        Test case IDs: R3.6.1, R3.6.2, R3.6.3, R3.6.4, R3.6.5
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
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
        """
        This page contains a form that a user can buy new tickets
        This page contains a form that a user can buy new tickets that requests field name
        This page contains a form that a user can buy new tickets that requests field quantity
        Test case IDs: R3.7.1, R3.7.2, R3.7.3
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        # click enter button
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # Validate that page contains element #buy-form
        self.assert_element('#buy-form')
        self.assert_element('#buy-form-name')
        self.assert_element('#buy-form-quantity')

    def test_ticket_update_form(self, *_):
        """
        This page contains a form that a user can update existing tickets
        This page contains a form that a user can update existing tickets which requests field name
        This page contains a form that a user can update existing tickets which requests field quantity
        This page contains a form that a user can update existing tickets which requests field price
        This page contains a form that a user can update existing tickets which requests field expiration date
        Test case IDs: R3.8.1, R3.8.2, R3.8.3, R3.8.4, R3.8.5
        """
        # Open /
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
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
        Test case ID: R3.9
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
        self.type('#sell-form-quantity', str(test_ticket.quantity))
        # Enter value into form_sell_price
        self.type('#sell-form-price', str(test_ticket.price))
        # Enter value into #form_sell_expiration_date
        self.type('#sell-form-expiration-date', test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="sell-form-submit"]')
        # Validate POST request sent to /sell
        self.assert_element('#welcome-header')

    def test_ticket_buy_post(self, *_):
        """
        The ticket-buying form can be posted to /buy
        Test case ID: R3.10
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_buy_name
        self.type('#buy-form-name', test_ticket.name)
        # Enter value into form_buy_quantity
        self.type('#buy-form-quantity', str(test_ticket.quantity))
        # Click #form_button
        self.click('input[id="buy-form-submit"]')
        # Validate POST request sent to /buy
        self.assert_element('#welcome-header')

    def test_ticket_update_post(self, *_):
        """
        The ticket-update form can be posted to /update
        Test case ID: R3.11
        """
        # Logout
        self.open(base_url + '/logout')
        # Open / and login
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # Enter value into form_update_name
        self.type("#update-form-name", test_ticket.name)
        # Enter value into form_update_quantity
        self.type("#update-form-quantity", str(test_ticket.quantity))
        # Enter value into form_update_price
        self.type("#update-form-price", str(test_ticket.price))
        # Enter value into #form_update_expiration_date
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        # Click #form_button
        self.click('input[id="update-form-submit"]')
        # Validate POST request sent to /update
        self.assert_element("#welcome-header")
