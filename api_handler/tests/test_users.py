import pytest
import json
import factory
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse

from api_handler.users.models import User


# automatically assigns @pytest.mark.django_db to every function
pytestmark = pytest.mark.django_db

class TestUsersAPI:

   def test_all_users_get(self, client):
      url = reverse('all_users')
      response = client.get(url)
      assert response.status_code == 200

   def test_users_post(self, client):

      expected_json = {
         "users":[{
         "first_name": "J",
         "last_name": "W"
         }]
      }
      print(expected_json)
      
      url = reverse('all_users')
      response = client.post(
         url,
         data=expected_json,
         format='json'
      )
      print(json.loads(response.content))
      assert response.status_code == 201


   def test_users_get(self, client):
      url = reverse('users', args='1')
      response = client.get(url)
      assert response.status_code == 200
