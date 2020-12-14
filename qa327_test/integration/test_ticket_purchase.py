import pytest
from seleniumbase import BaseCase
from qa327.models import User, Ticket

from qa327_test.conftest import base_url


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).

test_user = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password='Password123',
    balance=5000
)

test_ticket = Ticket(
    name='t1',
    quantity=50,
    price=70.50,
    expiration_date='20771210'
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

    def buy_ticket(self):
        """ Open base url and buy a ticket """
        self.open(base_url)
        self.type("#buy-form-name", test_ticket.name)
        self.type("#buy-form-quantity", str(test_ticket.quantity))
        self.click('input[id="buy-form-submit"]')

    def test_ticket_creation(self):
        """ This test checks the implemented login -> buy ticket feature """
        self.open(base_url + '/logout')
        self.register()
        self.login()
        self.buy_ticket()
        self.assert_text(test_ticket.name + " " + str(test_ticket.price))
