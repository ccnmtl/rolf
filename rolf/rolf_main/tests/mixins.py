from django.contrib.auth.models import User
from django.test import TestCase


class LoggedInTestMixin(TestCase):
    def setUp(self):
        self.u = User.objects.create(username='testuser')
        self.u.set_password('test')
        self.u.save()
        self.client.login(username='testuser', password='test')
