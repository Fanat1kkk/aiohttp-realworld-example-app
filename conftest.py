import pytest
from tortoise.contrib.test import finalizer, initializer
from conduit import settings


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(settings.MODELS, db_url=settings.DB_URL_TEST)
    request.addfinalizer(finalizer)
