import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import ProductFactory, UserFactory

# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db

INITIAL_USERS = 1
INITIAL_PRODUCTS = 3
TEST_PRODUCTS = 4

class TestUsersAPI(APITestCase):

    # Objects created in setUp function will persist throughout the test class
    # IMPORTANT: there's a preset user created in users/migrations with 2 products
    # It is reflected in the total_setup_users and total_setup_products variables
    def setUp(self):

        users = UserFactory.create_batch(3)
        for i in range(TEST_PRODUCTS):
            ProductFactory.create(user_id=users[i % 3])

        self.total_setup_users = len(users) + INITIAL_USERS
        self.total_setup_products = TEST_PRODUCTS + INITIAL_PRODUCTS

    # Test GET to get all products.
    def test_products_get_all(self):
        url = reverse('all_products')
        response = self.client.get(url)
        content = json.loads(response.content)

        assert response.status_code == 200
        assert len(content) == self.total_setup_products
        assert [1, 1, 1, 2, 3, 4, 2] == [product_info['user_id'] for product_info in content]

    # Test GET to get one or several products.
    def test_products_get_several(self):
        url = reverse('products', kwargs={'ids': '1,3'})
        response = self.client.get(url)
        content = json.loads(response.content)
        amount_of_users = len(content)

        assert response.status_code == 200
        assert amount_of_users == 2

    # Test POST. After creating a new product, 'product_id' should increment by 1.
    def test_products_post(self):
        url = reverse('all_products')
        response = self.client.get(url)
        products_before_post = len(json.loads(response.content))

        expected_json = {
            "products":
                [
                    {
                        "user_id": 3,
                        "product_type": "test",
                        "brand": "testing",
                        "model": "tested"
                    }
                ]
        }

        response = self.client.post(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content)[0]['product_id'] == products_before_post + 1

    # Test PUT. Should successfully update 'brand' and 'model'.
    def test_products_put(self):
        new_brand = 'Sony'
        new_model = 'MB-320'
        url = reverse('products', kwargs={'ids': '2'})

        expected_json = {
            "brand": new_brand,
            "model": new_model
        }

        response = self.client.put(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)['brand'] == new_brand
        assert json.loads(response.content)['model'] == new_model

    # Test DELETE on one or several ids. GETting respective ids should return 404.
    def test_products_delete_several(self):
        url = reverse('products', kwargs={'ids': '2,3'})
        response = self.client.delete(url)
        assert response.status_code == 200

        # Check that the users are really deleted
        url = reverse('products', kwargs={'ids': '2'})
        response = self.client.get(url)
        assert response.status_code == 404

        url = reverse('products', kwargs={'ids': '3'})
        response = self.client.get(url)
        assert response.status_code == 404

        url = reverse('all_products')
        response = self.client.get(url)
        amount_of_products = len(json.loads(response.content))
        assert amount_of_products == self.total_setup_products - 2

    # Test DELETE on all products. GETting all users should return an empty array.
    def test_products_delete_all(self):
        url = reverse('all_products')
        response = self.client.delete(url)
        assert response.status_code == 200

        url = reverse('all_products')
        response = self.client.get(url)
        amount_of_products = len(json.loads(response.content))
        assert response.status_code == 200
        assert amount_of_products == 0

    # Test DELETE on a user. Should lead to all products related to the user to be deleted as well.
    def test_products_delete_user(self):
        url = reverse('users', kwargs={'ids': '2'})
        self.client.delete(url)

        url = reverse('products', kwargs={'ids': '2,4'})
        response = self.client.get(url)
        assert response.status_code == 404
