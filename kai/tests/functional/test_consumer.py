from kai.tests import *

class TestConsumerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='consumer', action='index'))
        # Test response...
