from contextlib import contextmanager

from django.core.management import call_command


@contextmanager
def load_fixtures(*li):
    for i in li:
        call_command("loaddata", i)
        yield
