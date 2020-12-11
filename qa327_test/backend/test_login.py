from sys import base_exec_prefix
import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from qa327.backend import login_user

""" 
This white-box test uses condition coverage.

With login_user there is one if statement to watch out for, and two conditions. 

(not user): true or false
(not check_password_hash(user.password, password)): true or false

Both cannot be true at the same time, so this test will cover (true, false), (false, true), (false, false)
"""

test_user = User(
    email='tester0@gmail.com',
    name='Tester Zero',
    password='Password123',
    balance=5000
)


# In this case, the first condition will be true, meaning the or statement is true
@patch('qa327.backend.get_user', return_value=None)
def test_login_user_exist_false(self):
    return login_user(test_user.email, test_user.password) == None

# In this case, the second condition will be true, meaning the or statement is true


@patch('qa327.backend.get_user', return_value=test_user)
def test_login_password_match_false(self):
    return login_user(email=test_user.email, password="WrongPassword123") == None

# In this case both are false, meaning the if statements doesn't get executed


@patch('qa327.backend.get_user', return_value=test_user)
def test_login_success(self):
    return login_user(test_user.email, test_user.password) == test_user
