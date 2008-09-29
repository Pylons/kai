from kai.tests import *

class TestBuildbotController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='buildbot', action='index'))
        # Test response...
