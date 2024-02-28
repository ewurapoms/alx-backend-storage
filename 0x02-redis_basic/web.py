#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

from functools import wraps
import requests
import redis

store = redis.Redis()


def count_url_access(method):
    """ counts number of times a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


def get_page(url: str) -> str:
    """ prints HTML content of a url """
    res = requests.get(url)
    return res.text


get_page = count_url_access(get_page)
