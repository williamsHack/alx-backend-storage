#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""

import redis
import requests
from functools import wraps

def cache_and_track(expiration_time: int):
    """A decorator that implements an expiring web cache and tracker.

    Args:
        expiration_time: The expiration time in seconds.

    Returns:
        A decorator function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]

            # Check if the page is already cached.
            cache_key = f"cached:{url}"
            cached_page = redis.get(cache_key)
            if cached_page:
                # If the page is cached, return the cached value.
                return cached_page.decode("utf-8")

            # If the page is not cached, fetch it from the web.
            response = func(*args, **kwargs)
            response.raise_for_status()

            # Cache the page for the specified expiration time.
            redis.set(cache_key, response.content, ex=expiration_time)

            # Increment the access count for the page.
            count_key = f"count:{url}"
            redis.incr(count_key)

            return response.content

        return wrapper

    return decorator

@cache_and_track(expiration_time=10)
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    results = requests.get(url)
    return results.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
