import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import ProductFactory, UserFactory

# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db

INITIAL_USERS = 1
TEST_PRODUCTS = 3

class TestUsersAPI(APITestCase):

    # Objects created in setUp function will persist throughout the test class
    def setUp(self):
        users = UserFactory.create()
        for i in range(TEST_PRODUCTS):
            ProductFactory.create(user_id=users)

        self.mock_user_id = INITIAL_USERS + 1

    # Test GET to get all products of a certain user. Should return 2 different product items.
    def test_user_products_get(self):
        url = reverse('user_products', kwargs={'user_id': self.mock_user_id})
        response = self.client.get(url)
        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == TEST_PRODUCTS
