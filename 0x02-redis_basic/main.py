#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

get_page(URL)
get_page(URL)
get_page(URL)
get_page(URL)
get_page(URL)

local_redis = redis.Redis()
print(local_redis.get(key))
