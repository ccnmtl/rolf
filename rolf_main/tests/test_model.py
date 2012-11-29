from django.utils import unittest
from rolf_main.models import Category

class CategoryTest(unittest.TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test")

    def tearDown(self):
        self.c.delete()

    def test_basics(self):
        self.assertEquals(unicode(self.c), "test")
        self.assertEquals(self.c.get_absolute_url(),
                          "/category/%d/" % self.c.id)
