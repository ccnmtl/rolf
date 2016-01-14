from django.test import TestCase
from factories import CategoryFactory, ApplicationFactory, DeploymentFactory
from factories import UserFactory, RecipeFactory, ShellRecipeFactory
from factories import SettingFactory, StageFactory, PushFactory


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
        u = UserFactory(username='testuserce')
        self.assertFalse(d.can_edit(u))

    def test_can_push(self):
        d = DeploymentFactory()
        u = UserFactory(username='testuserce')
        self.assertFalse(d.can_push(u))

    def test_can_view(self):
        d = DeploymentFactory()
        u = UserFactory(username='testuserce')
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

    def test_clone_settings(self):
        s = SettingFactory()
        d1 = s.deployment
        d2 = DeploymentFactory()
        d1.clone_settings(d2)
        self.assertTrue(d2.setting_set.all().count() > 0)

    def test_clone_stage(self):
        s = StageFactory()
        d1 = s.deployment
        d2 = DeploymentFactory()
        d1.clone_stages(d2)
        self.assertTrue(d2.stage_set.all().count() > 0)

    def test_clear_old_pushes_below_threshold(self):
        p = PushFactory()
        d = p.deployment
        d.clear_old_pushes(keep=2)
        self.assertEqual(d.push_set.count(), 1)

    def test_clear_old_pushes_over_threshold(self):
        d = DeploymentFactory()
        PushFactory(deployment=d)
        PushFactory(deployment=d)
        PushFactory(deployment=d)
        d.clear_old_pushes(keep=2)
        self.assertEqual(d.push_set.count(), 2)


class BasicPushTest(TestCase):
    def test_push(self):
        self.u = UserFactory()
        self.d = DeploymentFactory()
        self.setting = SettingFactory(deployment=self.d)
        self.recipe = RecipeFactory()
        self.shell_recipe = ShellRecipeFactory()
        self.stage = StageFactory(
            deployment=self.d,
            recipe=self.recipe)
        self.stage2 = StageFactory(
            deployment=self.d,
            recipe=self.shell_recipe,
            name="test stage 2",
        )
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
        self.recipe = RecipeFactory()
        self.assertEquals(
            self.recipe.get_absolute_url(),
            "/cookbook/%d/" % self.recipe.id)

    def test_stage_absolute_url(self):
        self.stage = StageFactory()
        self.assertEquals(
            self.stage.get_absolute_url(),
            "/stage/%d/" % self.stage.id)

    def test_stage_all_recipes(self):
        self.shell_recipe = ShellRecipeFactory()
        self.stage = StageFactory()
        self.stage2 = StageFactory(recipe=self.shell_recipe)

        self.assertEquals(
            [r.id for r in self.stage.all_recipes()],
            [self.shell_recipe.id])
