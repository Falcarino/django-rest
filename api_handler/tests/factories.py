import factory
from django.contrib.auth import get_user_model
from products.models import Product


class UserFactory(factory.django.DjangoModelFactory):
    """
    Faker generates random data set by the appropriate topic

    List of available topics can be found here:
    https://faker.readthedocs.io/en/master/providers.html
    """
    class Meta:
        model = get_user_model()

    email = factory.faker.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '12345')


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Faker generates random data set by the appropriate topic

    List of available topics can be found here:
    https://faker.readthedocs.io/en/master/providers.html
    """
    class Meta:
        model = Product

    product_type = factory.faker.Faker('word')
    brand = factory.faker.Faker('word')
    model = factory.faker.Faker('license_plate')

