from kai.tests import *

class TestSnippetsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='snippets', action='index'))
        # Test response...
