from django.test import TestCase
from django.contrib.auth.models import User
from factories import CategoryFactory, ApplicationFactory, DeploymentFactory
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Setting, Stage, Recipe


class CategoryTest(TestCase):
    def test_basics(self):
        c = CategoryFactory()
        self.assertEquals(unicode(c), "test")
        self.assertEquals(c.get_absolute_url(),
                          "/category/%d/" % c.id)


class ApplicationTest(TestCase):
    def test_basics(self):
        a = ApplicationFactory()
        self.assertEquals(unicode(a), "test application")
        self.assertEquals(a.get_absolute_url(),
                          "/application/%d/" % a.id)

    def test_active_deployments(self):
        a = ApplicationFactory()
        self.assertEquals(a.active_deployments().count(), 0)


class DeploymentTest(TestCase):
    def test_basics(self):
        d = DeploymentFactory()
        self.assertEquals(unicode(d), "test deployment")
        self.assertEquals(d.get_absolute_url(),
                          "/deployment/%d/" % d.id)

    def test_all_categories(self):
        d = DeploymentFactory()
        self.assertEquals(d.all_categories().count(), 1)

    def test_status(self):
        d = DeploymentFactory()
        self.assertEquals(d.status(), "unknown")

    def test_last_message(self):
        d = DeploymentFactory()
        self.assertEquals(d.last_message(), None)

    def test_all_recipes(self):
        d = DeploymentFactory()
        self.assertEquals(d.all_recipes().count(), 0)

    def test_can_edit(self):
        d = DeploymentFactory()
        u = User.objects.create(username='testuserce')
        self.assertFalse(d.can_edit(u))

    def test_can_push(self):
        d = DeploymentFactory()
        u = User.objects.create(username='testuserce')
        self.assertFalse(d.can_push(u))

    def test_can_view(self):
        d = DeploymentFactory()
        u = User.objects.create(username='testuserce')
        self.assertFalse(d.can_view(u))

    def test_add_permission_form(self):
        d = DeploymentFactory()
        d.add_permission_form()

    def test_add_flag_form(self):
        d = DeploymentFactory()
        d.add_flag_form()

    def test_last_push_date(self):
        d = DeploymentFactory()
        self.assertEquals(d.last_push_date(), None)


class BasicPushTest(TestCase):
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
