import pytest
from seleniumbase import BaseCase
from qa327.models import User, Ticket

from qa327_test.conftest import base_url


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).

test_user = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password='Password123'
)

test_ticket = Ticket(
    name='Swagger',
    quantity=50,
    price=15.95,
    expiration_date="20210606"
)


@pytest.mark.usefixtures('server')
class Registered(BaseCase):
    def register(self):
        """register new user"""
        self.open(base_url + '/register')
        self.type("#email", test_user.email)
        self.type("#name", test_user.name)
        self.type("#password", test_user.password)
        self.type("#password2", test_user.password)
        self.click('input[type="submit"]')

    def login(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open(base_url + '/login')
        self.type("#email", test_user.email)
        self.type("#password", test_user.password)
        self.click('input[type="submit"]')

    def sell_ticket(self):
        """ Open base url and sell a ticket """
        self.open(base_url)
        self.type("#sell-form-name", test_ticket.name)
        self.type("#sell-form-quantity", test_ticket.quantity)
        self.type("#sell-form-price", test_ticket.price)
        self.type("#sell-form-expiration-date", test_ticket.expiration_date)
        self.click('input[id="sell-form-submit"]')

    def test_ticket_creation(self):
        """ This test checks the implemented login -> sell ticket feature """
        self.open(base_url + '/logout')
        self.register()
        self.login()
        self.sell_ticket()
        self.assert_text(test_ticket.name + " " + str(test_ticket.price))
