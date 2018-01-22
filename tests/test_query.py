import pytest

from tests.test_app.models import Owner


@pytest.mark.django_db
def test_two():
    assert Owner.objects.all().count() == 0
