import pytest
from pyramid.interfaces import IRequest
from typing_extensions import Annotated
from zope.interface import Interface, directlyProvides
from zope.interface.interfaces import ComponentLookupError


class IUser(Interface):
    pass


class INotRegistered(Interface):
    pass


class DummyUser:
    pass


@pytest.fixture
def active_user():
    return DummyUser()


@pytest.fixture
def user():
    return DummyUser()


@pytest.fixture(autouse=True)
def setup_registry(dummy_config, dummy_request, user, active_user):
    registry = dummy_config.registry

    registry.registerAdapter(lambda request: user, (IRequest,), IUser)
    registry.registerAdapter(
        lambda request: active_user, (IRequest,), IUser, name="active_user"
    )

    yield


def test_named_adapters_are_injected_in_function_views(
    view_mapper, active_user, dummy_request
):
    active_user_fixture = active_user

    def view(active_user: IUser):
        assert active_user is active_user_fixture

    mapped_view = view_mapper(view)
    mapped_view(None, dummy_request)


def test_unnamed_adapters_are_injected_in_function_views(
    view_mapper, user, dummy_request
):
    user_fixture = user

    def view(user: IUser):
        assert user is user_fixture

    mapped_view = view_mapper(view)
    mapped_view(None, dummy_request)


def test_named_adapters_are_injected_in_class_views(
    view_mapper, active_user, dummy_request
):
    active_user_fixture = active_user

    class View:
        def __init__(self, active_user: IUser):
            assert active_user is active_user_fixture

        def view(self):
            pass

    mapped_view = view_mapper(View)
    mapped_view(None, dummy_request)


def test_unnamed_adapters_are_injected_in_class_views(view_mapper, user, dummy_request):
    user_fixture = user

    class View:
        def __init__(self, user: IUser):
            assert user is user_fixture

        def view(self):
            pass

    mapped_view = view_mapper(View)
    mapped_view(None, dummy_request)


def test_unregistered_interfaces_raise_error(view_mapper, dummy_request):
    def view(user: INotRegistered):
        pass

    mapped_view = view_mapper(view)
    with pytest.raises(ComponentLookupError):
        mapped_view(None, dummy_request)


def test_annotated_types_use_interface(view_mapper, user, dummy_request):
    user_fixture = user

    def view(user: Annotated[DummyUser, IUser]):
        assert user is user_fixture

    mapped_view = view_mapper(view)

    mapped_view(None, dummy_request)


def test_exception_is_raised_if_no_zope_interface_is_found(
    view_mapper, user, dummy_request
):
    user_fixture = user

    def view(user: DummyUser):
        assert user is user_fixture

    mapped_view = view_mapper(view)

    with pytest.raises(ValueError):
        mapped_view(None, dummy_request)
