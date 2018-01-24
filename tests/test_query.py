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

    dic = {
        'path': '/graphql',
        'content_type': 'application/graphql',
    }

    test_client.post(data=query, **dic)

    query = """
    query{
        allNPets{
            edges{
                node{
                    id, 
                    name,
                    owner{
                        id,
                        firstName,
                    }
                }
            }
        }
    }
    """

    test_client.post(data=query, **dic)
