def lower(str):
    return str.lower() if str else None


DEFAULT = object()


def case(val, fun_dict):
    f = fun_dict.get(val)
    if f:
        return f()
    else:
        f = fun_dict.get(DEFAULT)
        return f() if f else None


def with_(val, f):
    return f(val) if val else None


def destruct(dict, *keys):
    return (dict.get(key) for key in keys)


def split(str):
    return str.split() if str else []


def join(seq, sep=' '):
    return sep.join(str(x) for x in seq) if seq else ''
