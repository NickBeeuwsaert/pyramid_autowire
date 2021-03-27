from inspect import signature


def _map_matchdict(fn, matchdict):
    fn_signature = signature(fn)

    for name, parameter in fn_signature.parameters.items():
        try:
            value = matchdict[name]
        except KeyError:
            continue
        yield (name, value)
