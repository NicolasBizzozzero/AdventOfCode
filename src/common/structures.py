from collections import defaultdict


def defaultdict_to_dict(obj: defaultdict) -> dict:
    for key in obj.keys():
        if isinstance(obj[key], defaultdict):
            obj[key] = dict(obj[key])
    obj = dict(obj)
    return obj
