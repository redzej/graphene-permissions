import pytest
from django.core.management import call_command
from django.test import Client

client = Client()


@pytest.mark.django_db
def test_n():
    call_command('loaddata', 'tests/fixtures/test_fixture.yaml')

    query = """
    allPets{
        edges{
            node{
                id,
                name,
            }
        }
    }
    """

    client.post('/graphql', data=query, content_type='application/graphql')
