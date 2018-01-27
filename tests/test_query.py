import pytest

from tests.utils import load_fixtures


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
])
@pytest.mark.django_db
def test_node_with_allow_any_access1(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        allOwners{
            edges{
                node{
                    id,
                    username,
                    firstName,
                }
            }
        }
    }
    """

    response = client.post(data=query, **test_kwargs)
    result = response.json()

    assert result['data'] == {
        'otherAllPets': {
            'edges': [
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6MQ==',
                    'name': 'Snakey',
                    'race': 'snake'}},
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6Mg==',
                    'name': 'Pawn',
                    'race': 'cat'}},
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6Mw==',
                    'name': 'Rex',
                    'race': 'dog'}}
            ]}
    }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'test'),
    ('kate', 'test'),
    ('paul', 'test'),
])
@pytest.mark.django_db
def test_node_with_allow_any_access2(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        otherAllPets{
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
        'otherAllPets': {
            'edges': [
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6MQ==',
                    'name': 'Snakey',
                    'race': 'snake'}},
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6Mg==',
                    'name': 'Pawn',
                    'race': 'cat'}},
                {'node': {
                    'id': 'SW5mb1BldE5vZGU6Mw==',
                    'name': 'Rex',
                    'race': 'dog'}}
            ]}
    }
