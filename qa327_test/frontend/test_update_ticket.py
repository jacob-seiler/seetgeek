from sys import base_exec_prefix
import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket
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


class BackEndUpdateTest(BaseCase):
    @patch('qa327.backend.update_ticket', return_value=True)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_is_valid(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - positive
        Test case IDs: R5.1.1, R5.2.1, R5.3.1, R5.4.1, R5.5.1
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Successfully updated ticket", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_is_not_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - negative
        Test case ID: R5.1.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", 'hello $$$')
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Name must have alphanumeric characters only.", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_name_is_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - negative
        Test case ID: R5.2.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name",
                  'thisis61characterslongaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Name must be less than 60 characters.", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_quantity_is_not_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - negative
        Test case ID: R5.3.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(0))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Quantity must be between 1 and 100.", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_price_is_not_valid(self, *_):
        """
        Price has to be of range [10, 100] - negative
        Test case ID: R5.4.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(0))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Price must be between 10 and 100 inclusive.", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_date_is_not_valid(self, *_):
        """
        Date must be given in the format YYYYMMDD - negative
        Test case ID: R5.5.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", '123456789')
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Date must be in the format YYYYMMDD.", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=True)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_does_exist(self, *_):
        """
        The ticket of the given name must exist - positive
        Test case ID: R5.6.1
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Successfully updated ticket", "#flash-message")

    @patch('qa327.backend.update_ticket', return_value=False)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_ticket_does_not_exist(self, *_):
        """
        The ticket of the given name must exist - negative
        Test case ID: R5.6.2
        """
        # Invalidate previous session
        self.open(base_url + '/logout')

        # Login user
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click("#btn-submit")

        # Open /
        self.open(base_url)

        # Update ticket info
        self.type("#update-form-name", 'fakeTicketName')
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click("#update-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Ticket does not exist.", "#flash-message")
