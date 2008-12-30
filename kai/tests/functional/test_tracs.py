from kai.tests import *

class TestTracsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tracs', action='index'))
        # Test response...
