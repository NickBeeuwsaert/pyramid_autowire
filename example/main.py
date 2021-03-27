from collections import Counter
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid_autowire import autowired
from zope.interface import Interface


class ICounter(Interface):
    pass


@view_config(
    route_name="index",
    mapper=autowired,
    renderer="json",
)
def index(counter: ICounter):
    return counter


@view_defaults(route_name="view_counter", mapper=autowired, renderer="json")
class ViewCounter:
    def __init__(self, /, counter: ICounter):
        self.counter = counter

    @view_config()
    def page(self, *, name):
        self.counter[name] += 1

        return {"message": f"Viewed {self.counter[name]} times."}


if __name__ == "__main__":
    config = Configurator()
    registry = config.registry

    registry.registerUtility(Counter(), ICounter)

    config.add_route("index", "/")
    config.add_route("view_counter", "view/{name}")

    config.scan(".")

    app = config.make_wsgi_app()

    server = make_server("0.0.0.0", 6543, app)
    server.serve_forever()
