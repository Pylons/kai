from kai.tests import *

class TestTracebacksController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tracebacks', action='index'))
        # Test response...
