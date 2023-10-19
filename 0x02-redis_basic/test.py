#!/usr/bin/python3
from exercise import Cache
cache = Cache()


data = "Hello, World!"
key = cache.store(data)
value = cache.get(key)
print(f"The key is{key}: and value is {value}")

new = 'ALAREEF'
store_key = cache.store(new)
print(f"{new} is stored with key: {store_key}")

def custom_converter(data):
    return data.decode()

converted_data = cache.get(key, fn=custom_converter)
print(f"Converted data: {converted_data}")

idan = 'Hello there'
idan_key = cache.store(idan)
idan_value = cache.get(idan_key)
print(f"idan key:{idan_key} idan value {idan_value}")
print(cache.get_str(idan_key))

number = '67'
print(type(number))
num_key = cache.store(number)
print(cache.get_int(num_key))
