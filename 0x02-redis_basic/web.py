#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
import requests
import redis

store = redis.Redis()


def count_url_access(func):
    """ counts number of times a URL is accessed """
    @wraps(func)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        update = f"count:{url}"
        html = func(url)

        store.incr(update)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ prints HTML content of a url """
    res = requests.get(url)
    return res.text
