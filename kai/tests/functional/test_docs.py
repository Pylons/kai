from kai.tests import *

class TestDocsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='docs', action='index'))
        # Test response...
