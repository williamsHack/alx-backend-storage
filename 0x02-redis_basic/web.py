import requests
import redis
from functools import wraps

# Initialize a Redis connection
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Define a decorator to cache and track URL accesses
def cache_and_track(url):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the URL is in the cache
            cached_data = r.get(f"cache:{url}")

            if cached_data:
                # If cached data exists, increment the access count
                r.incr(f"count:{url}")
                return cached_data.decode('utf-8')

            # If the URL is not in the cache, fetch the web page
            response = func(*args, **kwargs)

            # Store the web page content in the cache with a 10-second expiration
            r.setex(f"cache:{url}", 10, response)

            # Increment the access count
            r.incr(f"count:{url}")

            return response

        return wrapper

    return decorator

# Define the get_page function with the decorator
@cache_and_track("http://slowwly.robertomurray.co.uk")
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Test the get_page function
    for _ in range(5):
        content = get_page("http://slowwly.robertomurray.co.uk")
        print(content)

    # Get the access count for the URL
    access_count = r.get("count:http://slowwly.robertomurray.co.uk")
    print(f"Access count: {access_count.decode('utf-8')}")


