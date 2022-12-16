import factory

from products.models import Product
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Faker generates random data set by the appropriate topic

    List of available topics can be found here:
    https://faker.readthedocs.io/en/master/providers.html
    """
    email = factory.faker.Faker('email')
    password = factory.faker.Faker('password')

    class Meta:
        model = User


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Faker generates random data set by the appropriate topic

    List of available topics can be found here:
    https://faker.readthedocs.io/en/master/providers.html
    """
    product_type = factory.faker.Faker('word')
    brand = factory.faker.Faker('word')
    model = factory.faker.Faker('license_plate')

    class Meta:
        model = Product
