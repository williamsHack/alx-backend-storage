#!/usr/bin/env python3
"""
Caching request module with a Redis connection pool
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Create a Redis connection pool for improved performance
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_client = redis.Redis(connection_pool=redis_pool)

def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - checks whether a URL's data is cached
            - tracks how many times get_page is called
        """
        redis_key = f'cache:{url}'
        access_count_key = f'count:{url}'
        redis_client.incr(access_count_key)
        cached_page = redis_client.get(redis_key)
        
        if cached_page:
            return cached_page.decode('utf-8')
        
        response = fn(url)
        redis_client.setex(redis_key, 10, response)
        return response
    
    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """ Makes an HTTP request to a given endpoint
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the get_page function
    for _ in range(5):
        content = get_page("http://slowwly.robertomurray.co.uk")
        print(content)

    # Get the access count for the URL
    access_count = redis_client.get("count:http://slowwly.robertomurray.co.uk")
    print(f"Access count: {access_count.decode('utf-8')}")

