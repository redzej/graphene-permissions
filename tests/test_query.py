import pytest

from tests.utils import load_fixtures


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None)
])
@pytest.mark.django_db
def test_filter_staff_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        allStaffPets{
            edges{
                node{
                    id,
                    name,
                    race,
                }
            }
        }
    }
    """

    response = client.post(data=query, **test_kwargs)
    result = response.json()

    if login is 'tom':
        assert result['data'] == {
            'allStaffPets': {
                'edges': [
                    {'node': {
                        'id': 'U3RhZmZSZXF1aXJlZFBldE5vZGU6MQ==',
                        'name': 'Snakey',
                        'race': 'snake'}},
                    {'node': {
                        'id': 'U3RhZmZSZXF1aXJlZFBldE5vZGU6Mg==',
                        'name': 'Pawn',
                        'race': 'cat'}},
                    {'node': {
                        'id': 'U3RhZmZSZXF1aXJlZFBldE5vZGU6Mw==',
                        'name': 'Rex',
                        'race': 'dog'}}
                ]}
        }
    else:
        assert result['data'] == {
            'allStaffPets': {
                'edges': []
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_filter_allow_authenticated_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        allUserPets{
            edges{
                node{
                    id,
                    name,
                    race
                }
            }
        }
    }
    """

    response = client.post(data=query, **test_kwargs)
    result = response.json()

    if login in ('tom', 'kate', 'paul'):
        assert result['data'] == {
            'allUserPets': {
                'edges': [
                    {'node': {
                        'id': 'QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZTox',
                        'name': 'Snakey',
                        'race': 'snake'}},
                    {'node': {
                        'id': 'QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZToy',
                        'name': 'Pawn',
                        'race': 'cat'}},
                    {'node': {
                        'id': 'QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZToz',
                        'name': 'Rex',
                        'race': 'dog'}}
                ]}
        }
    else:
        assert result['data'] == {
            'allUserPets': {
                'edges': []
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'test'),
    ('kate', 'test'),
    ('paul', 'test'),
    (None, None),
])
@pytest.mark.django_db
def test_filter_allow_any_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        allPets{
            edges{
                node{
                    id,
                    name,
                    race
                }
            }
        }
    }
    """

    response = client.post(data=query, **test_kwargs)
    result = response.json()

    assert result['data'] == {
        'allPets': {
            'edges': [
                {'node': {
                    'id': 'QWxsb3dBbnlQZXROb2RlOjE=',
                    'name': 'Snakey',
                    'race': 'snake'}},
                {'node': {
                    'id': 'QWxsb3dBbnlQZXROb2RlOjI=',
                    'name': 'Pawn',
                    'race': 'cat'}},
                {'node': {
                    'id': 'QWxsb3dBbnlQZXROb2RlOjM=',
                    'name': 'Rex',
                    'race': 'dog'}}
            ]}
    }
