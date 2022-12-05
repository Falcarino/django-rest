import pytest
import json
import factory
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse

from .factories import ProductFactory, UserFactory


# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db

class TestUsersAPI(APITestCase):

    # Objects created in setUp function will persist throughout the test class
    def setUp(self):
        previous = None
        for _ in range(3):
            user = UserFactory.create()
            if previous is None:
                previous = user
            else:
                user = previous
                previous = None
            ProductFactory.create(user_id=user)

    # Test GET to get all users. Pre-set amount of users is 3
    def test_products_get_all(self):
        url = reverse('all_products')
        response = self.client.get(url)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 3
        assert 2 not in [product_info['user_id'] for product_info in content]
