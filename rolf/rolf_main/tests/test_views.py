from django.contrib.auth.models import Group
from django.test import TestCase
from django.test.client import Client
from factories import UserFactory, CategoryFactory, ApplicationFactory
from factories import DeploymentFactory


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class LoginTest(TestCase):
    def test_root(self):
        self.c = Client()
        self.u = UserFactory()
        self.u.set_password("test")
        self.u.save()

        self.c.login(username=self.u.username, password="test")
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)


class CrudTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = UserFactory(is_staff=True)
        self.u.set_password("test")
        self.u.save()
        # need to make the user have at least one group
        g = Group.objects.create(name=self.u.username)
        g.user_set.add(self.u)
        g.save()
        self.c.login(username=self.u.username, password="test")

    def test_category_crud(self):
        r = self.c.get("/")
        self.assertFalse("test category" in r.content)
        r = self.c.post("/category/add/", {'name': 'test category'})
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/")
        self.assertTrue("test category" in r.content)

    def test_application_crud(self):
        c = CategoryFactory()
        r = self.c.get(c.get_absolute_url())
        self.assertFalse("test application" in r.content)
        r = self.c.post(c.get_absolute_url() + "add_application/",
                        {'name': 'test application'})
        self.assertEqual(r.status_code, 302)
        r = self.c.get(c.get_absolute_url())
        self.assertTrue("test application" in r.content)

    def test_deployment_crud(self):
        a = ApplicationFactory()
        r = self.c.get(a.get_absolute_url())
        self.assertFalse("test deployment" in r.content)
        r = self.c.post(a.get_absolute_url() + "add_deployment/",
                        {'name': 'test deployment'})
        self.assertEqual(r.status_code, 302)
        r = self.c.get(a.get_absolute_url())
        self.assertTrue("test deployment" in r.content)

    def test_setting_crud(self):
        d = DeploymentFactory()
        d.add_editor(self.u)
        r = self.c.get(d.get_absolute_url())
        self.assertFalse("test setting" in r.content)
        r = self.c.post(d.get_absolute_url() + "add_setting/",
                        {'name': 'test setting', 'value': 'test value'})
        self.assertEqual(r.status_code, 302)
        r = self.c.get(d.get_absolute_url())
        self.assertTrue("test setting" in r.content)


class ApiTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = UserFactory()
        self.u.set_password("test")
        self.u.save()
        self.c.login(username=self.u.username, password="test")

    def test_plain_getkey(self):
        response = self.c.get("/api/1.0/get_key/")
        assert "<h2>Get API Key</h2>" in response.content

        # no ip specified, so there should be a form
        assert ("Alternatively, you can enter an IP address "
                "here and get a key") in response.content

    def test_key_for_other_ip(self):
        response = self.c.get("/api/1.0/get_key/?ip=128.59.1.1")
        assert ("This key is for the specified IP "
                "Address (128.59.1.1)") in response.content
