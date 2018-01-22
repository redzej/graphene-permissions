from tests.test_app.models import Owner
import pytest


@pytest.mark.django_db
def test_two():
    assert Owner.objects.all().count() == 0
