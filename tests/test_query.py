import pytest

from tests.utils import load_fixtures


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.django_db
def test_n(test_client):

    query = """
    query{
        allPets{
            edges{
                node{
                    id,
                    name,
                }
            }
        }
    }
    """

    test_client.post('/graphql', data=query, content_type='application/graphql')
