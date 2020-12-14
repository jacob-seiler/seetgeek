from sys import base_exec_prefix
import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket
from qa327.utils import validate_ticket
from qa327.backend import ticket_exists, enough_tickets, enough_balance
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

# Mock a sample ticket
test_ticket = Ticket(
    name='t1',
    quantity=50,
    price=70.50,
    expiration_date='20771210'
)

test_purchase_quantity = 5


class BackEndUpdateTest(BaseCase):
    def test_ticket_is_valid(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - positive
        Test case IDs: R6.1.1, R6.2.1, R6.3.1
        """
        return validate_ticket(test_ticket.name, test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == False

    def test_ticket_is_not_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - negative
        Test case ID: R6.1.2
        """
        return validate_ticket('hello $$$', test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == "Name must have alphanumeric characters only."

    def test_ticket_name_is_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - negative
        Test case ID: R6.2.2
        """
        return validate_ticket('thisis61characterslongaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', test_ticket.quantity, test_ticket.price, test_ticket.expiration_date) == "Name must be less than 60 characters."

    def test_ticket_quantity_is_not_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - negative
        Test case ID: R6.3.2
        """
        return validate_ticket(test_ticket.name, '0', test_ticket.price, test_ticket.expiration_date) == "Quantity must be between 1 and 100."

    def test_ticket_does_exist(self, *_):
        """
        The ticket of the given name must exist - positive
        Test case ID: R6.4.1
        """
        return ticket_exists(test_ticket.name)

    def test_ticket_does_not_exist(self, *_):
        """
        The ticket of the given name must exist - negative
        Test case ID: R6.4.2
        """
        return not ticket_exists('fakeTicketName')

    def test_ticket_quantity_is_enough(self, *_):
        """
        The quantity is more than the quantity requested to buy
        Test case ID: R6.5.1
        """
        return enough_tickets(test_ticket.name, 5)

    def test_ticket_quantity_is_not_enough(self, *_):
        """
        The quantity is less than the quantity requested to buy
        Test case ID: R6.5.2
        """
        return not enough_tickets(test_ticket.name, 100)

    def test_user_balance_is_enough(self, *_):
        """
        The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
        Test case ID: R6.6.1
        """
        return enough_balance(test_user.balance, test_ticket.price, 5)

    def test_user_balance_is_not_enough(self, *_):
        """
        The user does not have more balance than the ticket price * quantity + service fee (35%) + tax (5%)
        Test case ID: R6.6.2
        """
        return enough_balance(test_user.balance, test_ticket.price, 1000)
