from kai.tests import *

class TestArticlesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='articles', action='index'))
        # Test response...
