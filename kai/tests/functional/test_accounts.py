from kai.tests import *

class TestAccountsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='accounts', action='index'))
        # Test response...
