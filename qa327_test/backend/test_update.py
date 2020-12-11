from sys import base_exec_prefix
import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket
from qa327.utils import validate_ticket
from qa327.backend import ticket_exists
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
    def test_ticket_is_valid(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - positive
        """
        return validate_ticket(test_ticket.name, test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == False

    def test_ticket_is_not_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - negative
        """
        return validate_ticket('hello $$$', test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == "Name must have alphanumeric characters only."

    def test_ticket_name_is_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - negative
        """
        return validate_ticket('thisis61characterslongaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == "Name must be less than 60 characters."

    def test_ticket_quantity_is_not_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - negative
        """
        return validate_ticket(test_ticket.name, '0', test_ticket.price, test_ticket.expiration_date) == "Quantity must be between 1 and 100."

    def test_ticket_price_is_not_valid(self, *_):
        """
        Price has to be of range [10, 100] - negative
        """
        return validate_ticket(test_ticket.name, test_ticket.quantity, '0', test_ticket.expiration_date) == "Price must be between 10 and 100 inclusive."

    def test_ticket_date_is_not_valid(self, *_):
        """
        Date must be given in the format YYYYMMDD - negative
        """
        return validate_ticket(test_ticket.name, test_ticket.quantity, test_ticket.price, '123456789') == "Date must be in the format YYYYMMDD."

    def test_ticket_does_exist(self, *_):
        """
        The ticket of the given name must exist - positive
        """
        return ticket_exists(test_ticket.name)

    def test_ticket_does_not_exist(self, *_):
        """
        The ticket of the given name must exist - negative
        """
        return not ticket_exists('fakeTicketName')
