#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import requests
import time
from functools import wraps


def count_url_access(func):
    """ accessing function"""
    cache = {}

    def wrapper(url):
        """wrapper function"""
        if url in cache:
            # Check if cached entry is still valid (within 10 seconds)
            if time.time() - cache[url]['timestamp'] < 10:
                cache[url]['count'] += 1
                return cache[url]['content']

        # If not cached or expired, fetch the page content
        response = func(url)
        content = response.text

        # Update cache with new content and reset access count
        cache[url] = {'content': content, 'count': 1, 'timestamp': time.time()}

        return content

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ main function"""
    response = requests.get(url)
    return response


# Example usage
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/" \
      "http://www.example.com"
for _ in range(5):
    print(get_page(url))
