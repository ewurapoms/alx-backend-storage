#!/usr/bin/env python3
"""Module that handles redis operations and caches"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ displays script """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ returns a wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ stores function input and output"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ returns a wrapper function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """ displays replay script"""
    red = redis.Redis()
    placeholder = fn.__qualname__
    c = red.get(placeholder)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(placeholder, c))
    inputs = red.lrange("{}:inputs".format(placeholder), 0, -1)
    outputs = red.lrange("{}:outputs".format(placeholder), 0, -1)
    for inner, outer in zip(inputs, outputs):
        try:
            inner = inner.decode("utf-8")
        except Exception:
            inner = ""
        try:
            outer = outer.decode("utf-8")
        except Exception:
            outer = ""
        print("{}(*{}) -> {}".format(placeholder, inner, outer))


class Cache:
    """represents a Cache redis class"""
    def __init__(self):
        """displays the instance"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes a data argument and returns a string"""
        element = str(uuid4())
        self._redis.set(element, data)
        return element

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ performs a format reset """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ displays function"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """function displayed here"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
