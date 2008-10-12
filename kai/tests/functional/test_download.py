from kai.tests import *

class TestDownloadController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='download', action='index'))
        # Test response...
