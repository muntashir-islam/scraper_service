import requests
import time
import os
import random

# Configuration for the scraper_service and interval settings
SCRAPER_SERVICE_URL = os.getenv('SCRAPER_SERVICE_URL', 'http://localhost:8080')  # Default URL
REQUEST_INTERVAL = int(os.getenv('REQUEST_INTERVAL', '5'))  # Default interval (in seconds)

# List of target URLs to scrape
TARGET_URLS = [
    "https://phaidra.ai",
    "https://google.com",
    "https://github.com",
    "https://phaidra.ai/trackrecord",
    "https://wikipedia.org"
]


def make_scraper_request():
    """Send a request to scraper_service with a randomly selected URL."""
    target_url = random.choice(TARGET_URLS)  # Randomly select a target URL
    try:
        response = requests.post(
            SCRAPER_SERVICE_URL,
            json={"url": target_url}
        )
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Log the result of the scrape
        print(f"Scraped URL: {data.get('url')}")
        print(f"Status Code: {data.get('status_code')}")
        print(f"Content (first 200 chars): {data.get('content')[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"Error requesting scraper_service: {e}")


def main():
    """Main loop to periodically call the scraper_service."""
    print(f"Starting scraper service requests to {SCRAPER_SERVICE_URL} every {REQUEST_INTERVAL} seconds.")

    while True:
        make_scraper_request()
        time.sleep(REQUEST_INTERVAL)


if __name__ == "__main__":
    main()