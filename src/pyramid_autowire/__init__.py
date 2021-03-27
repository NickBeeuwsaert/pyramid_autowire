from .autowired_view import AutowiredView


class ViewMapper:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, view):
        return AutowiredView(view, self.kwargs.get("attr"))


autowired = ViewMapper


def includeme(config):
    """Change the default view mapper to our auto-wired viewmapper."""
    config.set_view_mapper(autowired)
