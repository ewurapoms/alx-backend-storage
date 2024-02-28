#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import requests
import time
from functools import wraps

# Dictionary to store cached pages and access counts
cache = {}


def cache_with_expiry(expiry=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            if url in cache:
                # Check if the cached entry is still valid (within expiry time)
                if time.time() - cache[url]['timestamp'] < expiry:
                    cache[url]['count'] += 1
                    return cache[url]['content']

            # If not cached or expired, fetch the page content
            content = func(url)

            # Update cache with new content and reset access count
            cache[url] = {
                'content': content,
                'count': 1,
                'timestamp': time.time()
            }
            return content

        return wrapper

    return decorator


@cache_with_expiry(expiry=10)
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL.

    The function uses the requests module to obtain
    the HTML content of the given URL.
    It also tracks the number of times the URL was
    accessed and caches the result with
    an expiration time of 10 seconds.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
