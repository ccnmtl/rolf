from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)


class LoginTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()

    def tearDown(self):
        self.u.delete()

    def test_root(self):
        self.c.login(username="testuser", password="test")
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)


class ApiTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.u.delete()

    def test_plain_getkey(self):
        response = self.c.get("/api/1.0/get_key/")
        assert "<h2>Get API Key</h2>" in response.content
