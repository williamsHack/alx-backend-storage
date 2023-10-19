#!/usr/bin/python3

from redis import Redis
import json

re = Redis(
    host='127.0.0.1',
    port=6379
)
re.select(3)
if re.ping():
    print("PONG")
else:
    print("Connection failed")

## SET key-value pair
re.set("name", "AlAreef")

# Get value
if re.exists("name"):
    print("exists")
else:
    print("Nowhere to be found")
print(re.get("name").decode())

new_dict = {
    "Age": "17",
    "complexion": "Dark",
    "name": "Al-Areef",
    "school": "ALX Africa",
    "experience": "Nine months",
    "languages": json.dumps(["python", "Javascript", "shell"]),  # Convert list to JSON-encoded string
    "framework": "flask/django"
}

# Use hset to store individual field-value pairs in the hash
for key, value in new_dict.items():
    re.hset("my_hash", key, value)

# Use hgetall to retrieve the entire hash
stored_dict = re.hgetall("my_hash")

# Decode byte strings to strings for printing
decoded_dict = {}
for key, value in stored_dict.items():
    if isinstance(value, bytes):
        decoded_dict[key.decode()] = value.decode()
    else:
        decoded_dict[key.decode()] = value

# Print the retrieved values
for key, value in decoded_dict.items():
    print(f"{key}: {value}")
