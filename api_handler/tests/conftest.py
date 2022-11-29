import pytest
from django.conf import settings
from rest_framework.test import APIClient

@pytest.fixture
def simple_test_fixture():
    return True

@pytest.fixture
def api_client():
    return APIClient
