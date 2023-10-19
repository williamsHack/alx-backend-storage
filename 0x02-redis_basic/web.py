#!/usr/bin/env python3
"""
Caching request module for a different URL
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a URL's data is cached
            - tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes an HTTP request to a different endpoint
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Example usage of the decorated get_page function
    url = "http://slowwly.robertomurray.co.uk"  # Replace with the desired URL
    content = get_page(url)
    print(content)

    # Get the access count for the URL
    client = redis.Redis()
    access_count = client.get(f'count:{url}')
    print(f"Access count for {url}: {access_count.decode('utf-8')}")

