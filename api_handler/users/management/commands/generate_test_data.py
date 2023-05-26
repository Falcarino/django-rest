import random
import factory

from django.db import transaction
from django.core.management.base import BaseCommand

from users.models import User
from tests.factories import UserFactory, ProductFactory

NUM_USERS = 3
NUM_PRODUCTS = 10


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating new data...")
        # Create all the users
        all_users = []
        for _ in range(NUM_USERS):
            email = factory.Faker('email').evaluate(None, None, {'locale': None})
            pwd = '12345'
            user = User.objects.create_user(email=email, password=pwd)
            all_users.append(user)

        for _ in range(NUM_PRODUCTS):
            user = random.choice(all_users)
            ProductFactory.create(user_id=user)
