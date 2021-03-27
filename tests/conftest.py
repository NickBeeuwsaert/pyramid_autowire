import pytest
from pyramid.testing import DummyRequest, testConfig
from pyramid_autowire import ViewMapper


@pytest.fixture
def view_mapper():
    return ViewMapper(attr="view")


@pytest.fixture
def dummy_request():
    return DummyRequest()


@pytest.fixture
def dummy_config(dummy_request):
    with testConfig(request=dummy_request) as config:
        yield config
