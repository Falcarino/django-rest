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
        users = UserFactory.create_batch(2)
        for i in range(3):
            ProductFactory.create(user_id=users[i % 2])

    # Test GET to get all users. Pre-set amount of users is 3
    def test_products_get_all(self):
        url = reverse('all_products')
        response = self.client.get(url)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == 3
        assert [1, 2, 1] == [product_info['user_id'] for product_info in content]
