import inspect
from functools import cached_property, partial
from inspect import Parameter

from .dependency_injection import _map_dependencies
from .matchdict_injection import _map_matchdict


def _filter_parameters(parameters, kind):
    return [parameter for parameter in parameters.values() if parameter.kind is kind]


class AutowiredView:
    def __init__(self, view, attr=None):
        self._view = view
        self._attr = attr

        if self._num_positional_only_args > 2:
            raise ValueError(
                f"View {view.__name__!r} should accept 1 or 2 positional-only "
                "arguments."
            )

    @cached_property
    def _signature(self) -> inspect.Signature:
        return inspect.signature(self._view)

    @cached_property
    def _num_positional_only_args(self):
        signature = self._signature
        return len(_filter_parameters(signature.parameters, Parameter.POSITIONAL_ONLY))

    @cached_property
    def _injection_args(self):
        signature = self._signature
        return _filter_parameters(signature.parameters, Parameter.POSITIONAL_OR_KEYWORD)

    def __call__(self, context, request):
        view = self._view
        dependencies = _map_dependencies(self._injection_args, request)

        if self._num_positional_only_args == 2:
            view = partial(view, context, request)
        if self._num_positional_only_args == 1:
            view = partial(view, request)

        if inspect.isclass(self._view):
            view = view(*dependencies)
            view = getattr(view, self._attr)
        else:
            view = partial(view, *dependencies)

        matchargs = dict(_map_matchdict(view, request.matchdict))

        return view(**matchargs)
