import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_kwargs():
    return {
        "path": "/graphql",
        "content_type": "application/graphql",
    }
