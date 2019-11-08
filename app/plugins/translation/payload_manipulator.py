import operator
from functools import reduce


def get_by_path(root, items):
    # Access a nested object in root by item sequence.
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    # Set a value in a nested object in root by item sequence.
    get_by_path(root, items[:-1])[items[-1]] = value


def flatten_dict(indict, pre=None):
    # convert dictionary into generator of lists of indices
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in flatten_dict(value, pre + [key]):
                    yield d
            elif isinstance(value, list):
                for v in value:
                    for d in flatten_dict(v,  pre + [key] + [value.index(v)]):
                        yield d
            else:
                yield pre + [key, value]
    elif isinstance(indict, list):
        for value in indict:
            for d in flatten_dict(value, pre + [value]):
                yield d
    else:
        yield pre + [indict]
