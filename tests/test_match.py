def test_matchdict_is_passed_as_keyword_only_args(view_mapper, dummy_request):
    def view(*, post_id):
        assert post_id == "POST_ID"

    mapped_view = view_mapper(view)
    dummy_request.matchdict = {"post_id": "POST_ID"}
    mapped_view(None, dummy_request)


def test_default_keyword_only_args_work(view_mapper, dummy_request):
    def view(*, post_id="default"):
        assert post_id == "default"

    mapped_view = view_mapper(view)
    dummy_request.matchdict = {}
    mapped_view(None, dummy_request)
