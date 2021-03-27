from typing_extensions import Annotated, get_args, get_origin
from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError


def _get_annotation_args(annotation):
    if get_origin(annotation) is Annotated:
        return get_args(annotation)
    return (annotation,)


def _find_parameter_interface(parameter):
    annotation = parameter.annotation

    for annotation in _get_annotation_args(annotation):
        if issubclass(annotation, Interface):
            return annotation
    raise ValueError(f"{parameter.name!r} doesn't have a zope Interface!")


def _find_utility(registry, iface, name):
    try:
        utility = registry.getUtility(iface, name)
    except ComponentLookupError:
        utility = registry.getUtility(iface)
    return utility


def _find_adapter(registry, iface, request, name):
    try:
        adapter = registry.getAdapter(request, iface, name)
    except ComponentLookupError:
        adapter = registry.getAdapter(request, iface)
    return adapter


def _map_dependencies(parameters, request):
    for parameter in parameters:
        iface = _find_parameter_interface(parameter)

        try:
            dependency = _find_utility(request.registry, iface, parameter.name)
        except ComponentLookupError:
            dependency = _find_adapter(request.registry, iface, request, parameter.name)

        yield dependency
