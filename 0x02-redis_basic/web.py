#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import requests
import time
from functools import wraps

# Dictionary to store cached results
cache = {}


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL.

    The function checks if the URL is cached and not expired.
    If the content is already cached, it returns the cached content.
    Otherwise, it makes a request to the URL, retrieves the HTML content,
    caches the result with a 10-second expiration time, and returns the content.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    if url in cache and cache[url]['expiration'] > time.time():
        cache[url]['count'] += 1
        return cache[url]['content']

    response = requests.get(url)
    content = response.text

    cache[url] = {'content': content, 'expiration': time.time() + 10, 'count': 1}

    return content


def cache_result(func):
    """
    Decorator to track URL access count and cache the result.

    The decorator wraps a function and adds caching and access count tracking behavior.
    It checks if the URL is already cached and not expired.
    If the content is cached, it returns the cached content.
    Otherwise, it calls the wrapped function to retrieve the content,
    caches the result with a 10-second expiration time, and returns the content.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: The wrapper function.
    """
    @wraps(func)
    def wrapper(url):
        if url in cache and cache[url]['expiration'] > time.time():
            cache[url]['count'] += 1
            return cache[url]['content']

        content = func(url)
        cache[url] = {'content': content, 'expiration': time.time() + 10, 'count': 1}
        return content

    return wrapper


@cache_result
def get_page_with_decorator(url: str) -> str:
    """
    Retrieve the HTML content of a URL using a decorator.

    This function is a decorated version that provides the same functionality as `get_page`.
    It uses the `cache_result` decorator to add caching and access count tracking behavior.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
