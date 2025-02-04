import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch

"""
This file defines all unit tests for the error pages.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""


class FrontEnd404PageTest(BaseCase):
    def test_error_404(self, *_):
        """
        This is a front end unit test to login to 404 error page.
        Test case ID: R8.1
        """
        # open an incorrect page
        self.open(base_url + '/error')
        # verify we get 404
        self.assert_text("Error 404", "#title")
