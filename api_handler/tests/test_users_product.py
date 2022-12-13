import json

import factory
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase

from .factories import ProductFactory, UserFactory

# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db


class TestUsersAPI(APITestCase):

    # Objects created in setUp function will persist throughout the test class
    def setUp(self):
        users = UserFactory.create_batch(3)
        for i in range(4):
            ProductFactory.create(user_id=users[i % 3])

    # Test GET to get all products of a certain user. Should return 2 different product items.
    def test_user_products_get(self):
        url = reverse('user_products', kwargs={'user_id': 1})
        response = self.client.get(url)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 2
