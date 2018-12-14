#!/usr/bin/env python3
import functools
import inspect

from typing import get_type_hints, Callable, Iterable
from collections import MutableMapping, defaultdict


OVERLOAD = "__overload__"


def get_key(itr: Iterable) -> tuple:
    return tuple(itr)


def dispatch(self, key, *args, **kwargs) -> Callable:
    key_new = get_key(map(type, args))
    try:
        method = self.__class__.__overload__[key][key_new]
    except KeyError:
        raise AttributeError("{} has no overloaded method '{} with args {}'".format(self, key, key_new))
    return method(self, *args, **kwargs)


class OverloadDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        # two-layer dict
        self._d[OVERLOAD] = defaultdict(dict)

    def __getitem__(self, key):
        return self._d[key]

    def _overload(self, key, method):
        typehints = get_type_hints(method)
        arg_types = (
            v for k, v in typehints.items()
            if k != "return"
        )
        key_new = get_key(arg_types)
        self._d[OVERLOAD][key][key_new] = method

    def __setitem__(self, key, value):
        """access the method definition"""
        if key in self._d and inspect.isfunction(value):
            # overload the method
            method = value
            if key not in self._d[OVERLOAD]:
                # rename the original method
                self._overload(key, self._d[key])
                self._d[key] = functools.partialmethod(dispatch, key)

            self._overload(key, method)
        else:
            self._d[key] = value

    def __delitem__(self, key):
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __contains__(self, key):
        return key in self._d

    def __repr__(self):
        return "{}:{}".format(type(self).__name__, self._d)


class  OverloadMeta(type):
    def __prepare__(cls, *args, **kwargs):
        return OverloadDict()

    def __new__(cls, name, bases, overload_dict: OverloadDict):
        return super().__new__(cls, name, bases, dict(overload_dict))
