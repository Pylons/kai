from kai.tests import *

class TestCommentsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='comments', action='index'))
        # Test response...
