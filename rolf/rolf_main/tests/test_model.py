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

    def test_active_deployments(self):
        self.assertEquals(self.a.active_deployments().count(), 0)


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

    def test_all_categories(self):
        self.assertEquals(self.d.all_categories().count(), 1)

    def test_status(self):
        self.assertEquals(self.d.status(), "unknown")

    def test_last_message(self):
        self.assertEquals(self.d.last_message(), None)

    def test_all_recipes(self):
        self.assertEquals(self.d.all_recipes().count(), 0)

    def test_can_edit(self):
        u = User.objects.create(username='testuserce')
        self.assertFalse(self.d.can_edit(u))
        u.delete()

    def test_can_push(self):
        u = User.objects.create(username='testuserce')
        self.assertFalse(self.d.can_push(u))
        u.delete()

    def test_can_view(self):
        u = User.objects.create(username='testuserce')
        self.assertFalse(self.d.can_view(u))
        u.delete()

    def test_add_permission_form(self):
        self.d.add_permission_form()

    def test_add_flag_form(self):
        self.d.add_flag_form()

    def test_last_push_date(self):
        self.assertEquals(self.d.last_push_date(), None)


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
            code="print 'hello'\nself.execute(['echo', 'foo'])",
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
        self.shell_recipe.delete()
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
        self.assertEquals(ps.stderr(), "")

        self.assertEquals(self.d.most_recent_push(), push)
        self.assertEquals(self.d.status(), push.status)
        self.assertEquals(self.d.last_message(), push.comment)
        self.assertEquals(self.d.last_push_date(), push.start_time)

        self.assertEquals(push.get_absolute_url(),
                          "/push/%d/" % push.id)

        push.run_stage(self.stage.id, rollback_id=self.stage.id)

        for pstage in push.reverse_pushstages():
            self.assertEquals(pstage.setting('foo'), '')

    def test_recipe_absolute_url(self):
        self.assertEquals(
            self.recipe.get_absolute_url(),
            "/cookbook/%d/" % self.recipe.id)

    def test_stage_absolute_url(self):
        self.assertEquals(
            self.stage.get_absolute_url(),
            "/stage/%d/" % self.stage.id)

    def test_stage_all_recipes(self):
        self.assertEquals(
            [r.id for r in self.stage.all_recipes()],
            [self.shell_recipe.id])
