import pytest
import json
import factory
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import path, include, reverse
from rest_framework import status

from rest_framework.test import APITestCase, URLPatternsTestCase
from api_handler.users.models import User


# automatically assigns @pytest.mark.django_db to every function
pytestmark = pytest.mark.django_db


class TestUsersAPI(APITestCase, URLPatternsTestCase):
   urlpatterns = [
      path('api/', include('api_handler.core.urls')),
   ]

   def setUp(self) -> None:
      url = reverse('all_users')
      self.client.post(
         url,
         data={
            "users":[{
               "first_name": "J",
               "last_name": "W"
            }]
         },
         format='json'
      )

   def test_all_users_get(self):
      url = reverse('all_users')
      response = self.client.get(url)
      assert response.status_code == 200

   def test_users_post(self):

      expected_json = {
         "users": [{
            "first_name": "J",
            "last_name": "W"
         }]
      }

      url = reverse('all_users')
      response = self.client.post(
         url,
         data=expected_json,
         format='json'
      )
      self.assertEqual(json.loads(response.content)[0]['user_id'], 2)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)


   def test_users_get(self):
      url = reverse('users', kwargs={'ids': '3'})
      print(url)
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
