import factory
from django.contrib.auth.models import User
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Recipe, Setting, Stage, Push


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category
    name = "test"


class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Application
    name = "test application"
    category = factory.SubFactory(CategoryFactory)


class DeploymentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Deployment
    name = "test deployment"
    application = factory.SubFactory(ApplicationFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'testuser{0}'.format(n))


class RecipeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Recipe
    name = "test recipe"
    language = "python"
    code = "print 'hello'\nself.execute(['echo', 'foo'])"
    description = ""


class ShellRecipeFactory(RecipeFactory):
    name = "test shell recipe"
    language = "shell"
    code = "echo $TEST_FOO"


class SettingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Setting
    name = "TEST_FOO"
    value = "TEST_BAR"
    deployment = factory.SubFactory(DeploymentFactory)


class StageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Stage
    name = "test stage"
    deployment = factory.SubFactory(DeploymentFactory)
    recipe = factory.SubFactory(RecipeFactory)


class PushFactory(factory.DjangoModelFactory):
    class Meta:
        model = Push
    user = factory.SubFactory(UserFactory)
    deployment = factory.SubFactory(DeploymentFactory)
