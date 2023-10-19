import redis
import requests
from functools import wraps

def cache_and_track(expiration_time: int):
    """
    A decorator that implements an expiring web cache and tracker.

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
            cached_page = redis_client.get(f"cached:{url}")
            if cached_page:
                # If the page is cached, return the cached value.
                return cached_page.decode("utf-8")

            # If the page is not cached, fetch it from the web.
            response = func(*args, **kwargs)
            response.raise_for_status()

            # Cache the page for the specified expiration time.
            redis_client.set(f"cached:{url}", response.content, ex=expiration_time)

            # Increment the access count for the page.
            redis_client.incr(f"count:{url}")

            return response.content

        return wrapper

    return decorator

redis_client = redis.Redis()

@cache_and_track(expiration_time=10)
def get_page(url: str) -> str:
    """
    Obtains the HTML content of a particular URL.

    Args:
        url: The URL of the web page.

    Returns:
        The HTML content of the web page.
    """

    response = requests.get(url)
    response.raise_for_status()

    return response.content

if __name__ == "__main__":
    # Get the HTML content of the Google homepage.
    google_homepage = get_page("https://www.google.com/")

    # Get the HTML content of the Wikipedia article on Python.
    wikipedia_python_article = get_page("https://en.wikipedia.org/wiki/Python")

