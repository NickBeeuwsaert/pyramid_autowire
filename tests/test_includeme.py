import pyramid_autowire
from pyramid.interfaces import IViewMapperFactory


def test_includeme(dummy_config):
    with dummy_config:
        dummy_config.include("pyramid_autowire")

    assert (
        dummy_config.registry.queryUtility(IViewMapperFactory)
        is pyramid_autowire.autowired
    )
