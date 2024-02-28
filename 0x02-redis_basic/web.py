#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import requests
import time
from functools import wraps

cache = {}


def get_page(url: str) -> str:
    """
    checks if the URL is cached and not expired
    and make the request and retrieve the HTML content
    """
    if url in cache and cache[url]['expiration'] > time.time():
        cache[url]['count'] += 1
        return cache[url]['content']
    response = requests.get(url)
    con = response.text
    cache[url] = {'content': con, 'expiration': time.time() + 10, 'count': 1}
    return con


def cache_result(func):
    """
    Decorator to track URL access count
    and cache the result
    """
    @wraps(func)
    def wrapper(url):
        if url in cac and cac[url]['expiration'] > time.time():
            cac[url]['count'] += 1
            return cac[url]['content']
        con = func(url)
        cac[url] = {'content': con, 'expiration': time.time() + 10, 'count': 1}
        return con
    return wrapper


@cache_result
def get_page_with_decorator(url: str) -> str:
    """ prints the output"""
    response = requests.get(url)
    return response.text
