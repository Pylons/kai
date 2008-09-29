from kai.tests import *

class TestPastesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pastes', action='index'))
        # Test response...
