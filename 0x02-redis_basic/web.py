#!/usr/bin/env python3
"""
Caching request module with separate caches for different URLs
"""
import redis
import requests
from functools import wraps
from typing import Callable

def track_get_page(cache_name: str) -> Callable:
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(url: str) -> str:
            client = redis.Redis()
            cache_key = f'{cache_name}:{url}'
            
            client.incr(f'count:{cache_key}')
            cached_page = client.get(cache_key)
            if cached_page:
                return cached_page.decode('utf-8')
            
            response = fn(url)
            client.setex(cache_key, 10, response)
            return response
        return wrapper
    return decorator

@track_get_page("default_cache")
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

@track_get_page("special_cache")
def get_special_page(url: str) -> str:
    response = requests.get(url)
    return response.text

