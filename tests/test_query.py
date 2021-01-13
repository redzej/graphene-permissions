import pytest

from tests.utils import load_fixtures


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_node_superuser_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        superuserPet(id: "U3VwZXJVc2VyUmVxdWlyZWRQZXROb2RlOjE="){
            name,
            race,
        }
    }
    """

    response = client.post(data=query, **test_kwargs)
    result = response.json()

    if login == "tom":

        assert result["data"] == {"superuserPet": {"name": "Snakey", "race": "snake"}}
    else:
        assert result["data"] == {"superuserPet": None}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_filter_superuser_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        allSuperuserPets{
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

    if login == "tom":
        assert result["data"] == {
            "allSuperuserPets": {
                "edges": [
                    {
                        "node": {
                            "id": "U3VwZXJVc2VyUmVxdWlyZWRQZXROb2RlOjE=",
                            "name": "Snakey",
                            "race": "snake",
                        }
                    },
                    {
                        "node": {
                            "id": "U3VwZXJVc2VyUmVxdWlyZWRQZXROb2RlOjI=",
                            "name": "Pawn",
                            "race": "cat",
                        }
                    },
                    {
                        "node": {
                            "id": "U3VwZXJVc2VyUmVxdWlyZWRQZXROb2RlOjM=",
                            "name": "Rex",
                            "race": "dog",
                        }
                    },
                ]
            }
        }
    else:
        assert result["data"] == {"allSuperuserPets": {"edges": []}}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_node_staff_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        staffPet(id: "U3RhZmZSZXF1aXJlZFBldE5vZGU6MQ=="){
            name,
            race,
        }
    }
    """
    response = client.post(data=query, **test_kwargs)
    result = response.json()

    if login == "tom":
        assert result["data"] == {"staffPet": {"name": "Snakey", "race": "snake"}}
    else:
        assert result["data"] == {"staffPet": None}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
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

    if login == "tom":
        assert result["data"] == {
            "allStaffPets": {
                "edges": [
                    {
                        "node": {
                            "id": "U3RhZmZSZXF1aXJlZFBldE5vZGU6MQ==",
                            "name": "Snakey",
                            "race": "snake",
                        }
                    },
                    {
                        "node": {
                            "id": "U3RhZmZSZXF1aXJlZFBldE5vZGU6Mg==",
                            "name": "Pawn",
                            "race": "cat",
                        }
                    },
                    {
                        "node": {
                            "id": "U3RhZmZSZXF1aXJlZFBldE5vZGU6Mw==",
                            "name": "Rex",
                            "race": "dog",
                        }
                    },
                ]
            }
        }
    else:
        assert result["data"] == {"allStaffPets": {"edges": []}}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_node_allow_authenticated_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        userPet(id: "QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZTox"){
            name,
            race,
        }
    }
    """
    response = client.post(data=query, **test_kwargs)
    result = response.json()

    if login in ("tom", "kate", "paul"):
        assert result["data"] == {"userPet": {"name": "Snakey", "race": "snake"}}
    else:
        assert result["data"] == {"userPet": None}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
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

    if login in ("tom", "kate", "paul"):
        assert result["data"] == {
            "allUserPets": {
                "edges": [
                    {
                        "node": {
                            "id": "QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZTox",
                            "name": "Snakey",
                            "race": "snake",
                        }
                    },
                    {
                        "node": {
                            "id": "QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZToy",
                            "name": "Pawn",
                            "race": "cat",
                        }
                    },
                    {
                        "node": {
                            "id": "QWxsb3dBdXRoZW50aWNhdGVkUGV0Tm9kZToz",
                            "name": "Rex",
                            "race": "dog",
                        }
                    },
                ]
            }
        }
    else:
        assert result["data"] == {"allUserPets": {"edges": []}}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_node_allow_any_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        pet(id: "QWxsb3dBbnlQZXROb2RlOjE="){
            name,
            race,
        }
    }
    """
    response = client.post(data=query, **test_kwargs)
    result = response.json()

    assert result["data"] == {"pet": {"name": "Snakey", "race": "snake"}}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
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

    assert result["data"] == {
        "allPets": {
            "edges": [
                {
                    "node": {
                        "id": "QWxsb3dBbnlQZXROb2RlOjE=",
                        "name": "Snakey",
                        "race": "snake",
                    }
                },
                {
                    "node": {
                        "id": "QWxsb3dBbnlQZXROb2RlOjI=",
                        "name": "Pawn",
                        "race": "cat",
                    }
                },
                {
                    "node": {
                        "id": "QWxsb3dBbnlQZXROb2RlOjM=",
                        "name": "Rex",
                        "race": "dog",
                    }
                },
            ]
        }
    }


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "login, password",
    [
        ("tom", "testpassword"),
        ("kate", "testpassword"),
        ("paul", "testpassword"),
        (None, None),
    ],
)
@pytest.mark.django_db
def test_node_non_existent_object(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    query = """
    query{
        pet(id: "QWxsb3dBbnlQZXROb2RlOjE1"){
            name,
            race,
        }
    }
    """
    response = client.post(data=query, **test_kwargs)
    result = response.json()

    assert result["data"] == {"pet": None}


@load_fixtures("tests/fixtures/test_fixture.yaml")
@pytest.mark.parametrize(
    "query_name, id, expected",
    [
        (
            "allowOrNotAllowPet",
            "QWxsb3dPck5vdEFsbG93UGV0Tm9kZTox",
            {"allowOrNotAllowPet": {"name": "Snakey"}},
        ),
        (
            "allowAndNotAllowPet",
            "QWxsb3dBbmROb3RBbGxvd1BldE5vZGU6MQ==",
            {"allowAndNotAllowPet": None},
        ),
        (
            "allowAndNotNotAllowPet",
            "QWxsb3dBbmROb3ROb3RBbGxvd1BldE5vZGU6MQ==",
            {"allowAndNotNotAllowPet": {"name": "Snakey"}},
        ),
        (
            "notNotAllowPet",
            "Tm90Tm90QWxsb3dQZXROb2RlOjE=",
            {"notNotAllowPet": {"name": "Snakey"}},
        ),
    ],
)
@pytest.mark.django_db
def test_permission_operator_composing(client, test_kwargs, query_name, id, expected):
    client.login(username="tom", password="testpassword")
    query = """
    query{
        %s(id: "%s"){
            name,
        }
    }
    """ % (
        query_name,
        id,
    )
    response = client.post(data=query, **test_kwargs)
    result = response.json()
    assert result["data"] == expected
