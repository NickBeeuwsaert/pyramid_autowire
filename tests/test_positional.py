import pytest


@pytest.fixture
def dummy_context():
    return object()


def test_single_argument_gets_request_for_function_view(
    dummy_context, dummy_request, view_mapper
):
    def view(request, /):
        assert request is dummy_request

    mapped_view = view_mapper(view)

    mapped_view(dummy_context, dummy_request)


def test_two_arguments_gets_context_and_request_for_function_view(
    dummy_context, dummy_request, view_mapper
):
    def view(context, request, /):
        assert context is dummy_context
        assert request is dummy_request

    mapped_view = view_mapper(view)

    mapped_view(dummy_context, dummy_request)


def test_more_than_two_arguments_raises_error_for_function_view(view_mapper):
    def view(context, request, additional, /):
        pass

    with pytest.raises(ValueError):
        mapped_view = view_mapper(view)


def test_single_argument_gets_request_for_class_view(
    dummy_context, dummy_request, view_mapper
):
    class View:
        def __init__(self, request, /):
            assert request is dummy_request

        def view(self):
            pass

    mapped_view = view_mapper(View)

    mapped_view(dummy_context, dummy_request)


def test_two_arguments_gets_context_and_request_for_class_view(
    dummy_context, dummy_request, view_mapper
):
    class View:
        def __init__(self, context, request, /):
            assert context is dummy_context
            assert request is dummy_request

        def view(self):
            pass

    mapped_view = view_mapper(View)

    mapped_view(dummy_context, dummy_request)


def test_more_than_two_arguments_raises_error_for_class_view(view_mapper):
    class View:
        def __init__(self, context, request, too_many, /):
            pass

    with pytest.raises(ValueError):
        mapped_view = view_mapper(View)
