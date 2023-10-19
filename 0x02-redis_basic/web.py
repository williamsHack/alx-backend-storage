#!/usr/bin/env python3
"""
Caching request module for a different URL with 30-second cache expiration
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
        client.set(f'{url}', response, 30)  # Cache with a 30-second expiration
        return response

    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """ Makes an HTTP request to a given endpoint
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the get_page function with a different URL
    for _ in range(5):
        content = get_page("http://slowwly.robertomurray.co.uk")  # Replace with your desired URL
        print(content)

    # Get the access count for the URL
    access_count = redis.Redis().get("count:http://slowwly.robertomurray.co.uk")  # Replace with your desired URL
    print(f"Access count: {access_count.decode('utf-8')}")

