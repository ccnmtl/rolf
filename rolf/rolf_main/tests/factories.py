import factory
from django.contrib.auth.models import User
from rolf.rolf_main.models import Category, Application, Deployment
from rolf.rolf_main.models import Recipe, Setting, Stage


class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category
    name = "test"


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application
    name = "test application"
    category = factory.SubFactory(CategoryFactory)


class DeploymentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Deployment
    name = "test deployment"
    application = factory.SubFactory(ApplicationFactory)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = 'testuser'


class RecipeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Recipe
    name = "test recipe"
    language = "python"
    code = "print 'hello'\nself.execute(['echo', 'foo'])"
    description = ""


class ShellRecipeFactory(RecipeFactory):
    name = "test shell recipe"
    language = "shell"
    code = "echo $TEST_FOO"


class SettingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Setting
    name = "TEST_FOO"
    value = "TEST_BAR"
    deployment = factory.SubFactory(DeploymentFactory)


class StageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Stage
    name = "test stage"
    deployment = factory.SubFactory(DeploymentFactory)
    recipe = factory.SubFactory(RecipeFactory)
