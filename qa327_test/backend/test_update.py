from sys import base_exec_prefix
import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User, Ticket
from qa327.backend import get_user, register_user, create_ticket
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
    password='Password123'
)

# Moch a sample ticket
test_ticket = Ticket(
    name='t1',
    quantity=50,
    price=70.50,
    expiration_date='20771210'
)


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
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
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
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", 'hello $$$')
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text(
            "Name must have alphanumeric characters only.", "#flash-message")

    def test_ticket_name_is_not_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_name_is_too_long(self, *_):
        """
        The name of the ticket is no longer than 60 characters - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name",
                  "thisis61characterslongaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text(
            "Name must be less than 60 characters.", "#flash-message")

    def test_ticket_quantity_is_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_quantity_is_not_valid(self, *_):
        """
        The quantity of the tickets has to be more than 0, and less than or equal to 100. - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", '0')
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text(
            "Quantity must be between 1 and 100.", "#flash-message")

    def test_ticket_price_is_valid(self, *_):
        """
        Price has to be of range [10, 100] - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_price_is_not_valid(self, *_):
        """
        Price has to be of range [10, 100] - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", '0')
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text(
            "Price must be between 10 and 100 inclusive.", "#flash-message")

    def test_ticket_date_is_valid(self, *_):
        """
        Date must be given in the format YYYYMMDD - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_date_is_not_valid(self, *_):
        """
        Date must be given in the format YYYYMMDD - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", '123456789')
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text(
            "Date must be in the format YYYYMMDD.", "#flash-message")

    def test_ticket_does_exist(self, *_):
        """
        The ticket of the given name must exist - positive
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", test_ticket.name)
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Successfully updated ticket", "#flash-message")

    def test_ticket_does_not_exist(self, *_):
        """
        The ticket of the given name must exist - negative
        """
        # open /logout (to invalidate any logged-in sessions that may exist)
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter test_user's email and password and submit
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')
        # open /
        self.open(base_url)
        # enter test_ticket's info into the update form and submit
        self.type("#update-form-name", "fakeTicketName")
        self.type("#update-form-quantity", str(test_ticket.quantity))
        self.type("#update-form-price", str(test_ticket.price))
        self.type("#update-form-expiration-date", test_ticket.expiration_date)
        self.click('#update-form-submit')
        # validate that the #flash-message element shows 'Ticket does not exist.'
        self.assert_text("Ticket does not exist.", "#flash-message")
