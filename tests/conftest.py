import pytest
from django.test import Client


@pytest.fixture
def test_client():
    return Client()
