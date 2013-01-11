from smoketest import SmokeTest
from models import Deployment


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Deployment.objects.all().count()
        self.assertTrue(cnt > 0)
