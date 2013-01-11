from django.utils import unittest
from django.contrib.auth.models import User
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Setting, Stage, Recipe


class CategoryTest(unittest.TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test")

    def tearDown(self):
        self.c.delete()

    def test_basics(self):
        self.assertEquals(unicode(self.c), "test")
        self.assertEquals(self.c.get_absolute_url(),
                          "/category/%d/" % self.c.id)


class ApplicationTest(unittest.TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test category")
        self.a = Application.objects.create(name="test application",
                                            category=self.c)

    def tearDown(self):
        self.a.delete()
        self.c.delete()

    def test_basics(self):
        self.assertEquals(unicode(self.a), "test application")
        self.assertEquals(self.a.get_absolute_url(),
                          "/application/%d/" % self.a.id)


class DeploymentTest(unittest.TestCase):
    def setUp(self):
        self.c = Category.objects.create(name="test category")
        self.a = Application.objects.create(name="test application",
                                            category=self.c)
        self.d = Deployment.objects.create(name="test deployment",
                                           application=self.a)

    def tearDown(self):
        self.d.delete()
        self.a.delete()
        self.c.delete()

    def test_basics(self):
        self.assertEquals(unicode(self.d), "test deployment")
        self.assertEquals(self.d.get_absolute_url(),
                          "/deployment/%d/" % self.d.id)


class BasicPushTest(unittest.TestCase):
    def setUp(self):
        self.u = User.objects.create(username='testuser')
        self.c = Category.objects.create(name="test category")
        self.a = Application.objects.create(name="test application",
                                            category=self.c)
        self.d = Deployment.objects.create(name="test deployment",
                                           application=self.a)
        self.setting = Setting.objects.create(
            deployment=self.d, name="TEST_FOO",
            value="TEST_BAR"
        )
        self.recipe = Recipe.objects.create(
            name="test recipe",
            language="python",
            code="print 'hello'",
            description="",
        )
        self.shell_recipe = Recipe.objects.create(
            name="test shell recipe",
            language="shell",
            code="echo $TEST_FOO",
            description="",
        )
        self.stage = Stage.objects.create(
            deployment=self.d,
            recipe=self.recipe,
            name="test stage",
        )
        self.stage2 = Stage.objects.create(
            deployment=self.d,
            recipe=self.shell_recipe,
            name="test stage 2",
        )

    def tearDown(self):
        self.stage.delete()
        self.recipe.delete()
        self.setting.delete()
        self.d.delete()
        self.a.delete()
        self.c.delete()
        self.u.delete()

    def test_push(self):
        push = self.d.new_push(self.u, "test push")
        # haven't run anything so it should be inprogress
        self.assertEquals(push.status, "inprogress")
        for s in self.d.stage_set.all():
            push.run_stage(s.id)
        # should have completed successfully
        self.assertEquals(push.status, "ok")
        # and let's make sure a setting variable has round-tripped
        ps = push.pushstage_set.get(stage=self.stage2)
        self.assertEquals(ps.stdout(), "TEST_BAR\n")
