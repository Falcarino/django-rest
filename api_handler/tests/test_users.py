import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import UserFactory

# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db

INITIAL_USERS = 1


class TestUsersAPI(APITestCase):

    # Objects created in setUp function will persist throughout the test class
    def setUp(self):
        users = UserFactory.create_batch(3)
        self.total_setup_users = len(users) + INITIAL_USERS

    # Test GET to get all users. Pre-set amount of users is 3 + $DJANGO_SU_EMAIL
    def test_users_get_all(self):
        url = reverse('all_users')
        response = self.client.get(url)
        amount_of_users = len(json.loads(response.content))

        assert response.status_code == 200
        assert amount_of_users == self.total_setup_users

    # Test GET to get one or several user.
    def test_users_get_several(self):
        url = reverse('users', kwargs={'ids': '1,3'})
        response = self.client.get(url)
        amount_of_users = len(json.loads(response.content))

        assert response.status_code == 200
        assert amount_of_users == 2

    # Test POST. After creating a new user, 'user_id' should increment by 1.
    def test_users_post(self):
        url = reverse('all_users')

        expected_json = {
            "users": [{
                "email": "jajabinks@star.com",
                "password": "12311asdacwee"
            }]
        }

        response = self.client.post(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content)[0]['user_id'] == self.total_setup_users + 1

    # Test PUT. Should successfully update 'first_name'.
    def test_users_put(self):
        new_email = "R2D2@milleniumfalcon.com"
        url = reverse('users', kwargs={'ids': '2'})

        expected_json = {"email": "R2D2@milleniumfalcon.com"}
        response = self.client.put(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)['email'] == new_email

    # Test DELETE on one or several ids. GETting respective ids should return 404.
    def test_users_delete_several(self):
        url = reverse('users', kwargs={'ids': '2,3'})
        response = self.client.delete(url)
        assert response.status_code == 200

        # Check that the users are really deleted
        url = reverse('users', kwargs={'ids': '2'})
        response = self.client.get(url)
        assert response.status_code == 404

        url = reverse('users', kwargs={'ids': '3'})
        response = self.client.get(url)
        assert response.status_code == 404

        url = reverse('all_users')
        response = self.client.get(url)
        amount_of_users = len(json.loads(response.content))
        assert amount_of_users == self.total_setup_users - 2

    # Test DELETE on all users. GETting all users should return an empty array.
    def test_users_delete_all(self):
        url = reverse('all_users')
        response = self.client.delete(url)
        assert response.status_code == 200

        url = reverse('all_users')
        response = self.client.get(url)
        amount_of_users = len(json.loads(response.content))
        assert response.status_code == 200
        assert amount_of_users == 0
