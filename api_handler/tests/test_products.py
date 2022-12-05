import pytest
import json
import factory
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse

from .factories import ProductFactory


# Automatically assigns @pytest.mark.django_db to every function
# But apparently the suite will work without it???
# pytestmark = pytest.mark.django_db

class TestUsersAPI(APITestCase):
   
   # Objects created in setUp function will persist throughout the test class
   def setUp(self):
      ProductFactory.create_batch(3)
   
   # Test GET to get all users. Pre-set amount of users is 3
   def test_products_get_all(self):
      url = reverse('all_products')
      response = self.client.get(url)
      amount_of_users = len(json.loads(response.content))

      print(json.loads(response.content))
      assert False
      
      assert response.status_code == 200
      assert amount_of_users == 3
