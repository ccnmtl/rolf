import factory
from rolf.rolf_main.models import Category, Application, Deployment


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
