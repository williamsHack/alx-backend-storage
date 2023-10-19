#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

# #!/usr/bin/env python3
# """ Main file """

# Cache = __import__('exercise').Cache

# cache = Cache()

# cache.store(b"first")
# print(cache.get(cache.store.__qualname__))

# cache.store(b"second")
# cache.store(b"third")
# print(cache.get(cache.store.__qualname__))
