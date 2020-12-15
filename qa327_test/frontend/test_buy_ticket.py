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
    password='Password123',
    balance=5000
)

# Mock a sample ticket
test_ticket = Ticket(
    name='ticket',
    quantity=200,
    price=50.00,
    expiration_date='20771210'
)


class FrontEndHomePageTest(BaseCase):
    def test_ticket_is_valid(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - positive
        Test case ID: R6.1.1
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        # Check that ticket is updated
        self.assert_text_visible(
            "Successfully bought ticket", "#flash-message")
        
    def test_ticket_is_not_alphanumeric(self, *_):
        """
        The name of the ticket has to be alphanumeric-only - negative
        Test case ID: R6.1.2
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

        # Buy ticket 
        self.type("#buy-form-name", "ticket!")
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Name must have alphanumeric characters only.", "#flash-message")

    def test_ticket_name_is_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - negative
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

        # Buy ticket 
        self.type("#buy-form-name", "thisis61characterslongaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Name must have alphanumeric characters only.", "#flash-message")

    def test_ticket_quantity_is_not_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - negative
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Name must have alphanumeric characters only.", "#flash-message")

    def test_ticket_does_exist(self, *_):
        """
        The ticket of the given name must exist - positive
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Successfully bought ticket.", "#flash-message")

    def test_ticket_does_not_exist(self, *_):
        """
        The ticket of the given name must exist - negative
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

        # Buy ticket 
        self.type("#buy-form-name", "ticket1")
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Ticket does not exist.", "#flash-message")

    def test_ticket_quantity_is_enough(self, *_):
        """
        The quantity is more than the quantity requested to buy
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity)+1)
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "The request quantity is not available.", "#flash-message")

    def test_ticket_quantity_is_not_enough(self, *_):
        """
        The quantity is less than the quantity requested to buy
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity)+1)
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Successfully bought ticket.", "#flash-message")


    def test_user_balance_is_enough(self, *_):
        """
        The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Successfully bought ticket.", "#flash-message")

    def test_user_balance_is_not_enough(self, *_):
        """
        The user does not have more balance than the ticket price * quantity + service fee (35%) + tax (5%)
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

        # Buy ticket 
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click("#buy-form-submit")

        self.assert_text_visible(
            "Insufficient balance.", "#flash-message")

