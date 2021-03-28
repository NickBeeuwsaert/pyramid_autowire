from weakref import WeakKeyDictionary


class cached_property:
    def __init__(self, cached_method):
        self._cached_method = cached_method
        self._map = WeakKeyDictionary()

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        try:
            value = self._map[instance]
        except KeyError:
            value = self._cached_method(instance)
            self._map[instance] = value

        return value
