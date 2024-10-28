#!/usr/bin/env python3
from flask import Flask, request, jsonify
import argparse
import requests
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("scraper_service")

METRICS_SERVICE_URL = os.getenv('METRICS_SERVICE_URL', 'http://localhost:9095/increment')
@app.route('/', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')  # Get JSON data from request

    if not url:
        error_message = 'No url provided'
        logger.warning(error_message)
        return jsonify({'error': error_message}), 400
    logger.info(f"Received request to scrape URL: {url}")

    try:
        response = requests.get(url)  # Fetch HTML content of the provided URL
        status_code = str(response.status_code)
        # Log the response status code
        logger.info(f"Fetched URL: {url} with status code: {status_code}")

        increment_response = requests.post(METRICS_SERVICE_URL, json={"url": url, "code": status_code})
        if increment_response.status_code != 200:
            error_message = "Failed to increment metric"
            logger.error(error_message)
            return jsonify({"error": error_message}), 500

        logger.info(f"Metric incremented for URL: {url} with status code: {status_code}")
        return jsonify({
            "url": url,
            "status_code": response.status_code,
            "content": response.text[:200]  # Return first 200 characters of the response
        })
    except requests.exceptions.RequestException as e:
        # Handle network issues
        logger.error(f"Error fetching URL {url}: {e}")
        return jsonify({"error": str(e)}), 500


def main():
    parser = argparse.ArgumentParser(description='Run the scraper service')
    parser.add_argument('--listen', type=str, default=":8080", help='Host and the port number to listen on')
    args = parser.parse_args()

    host, port = args.listen.split(':')  # Extract host and port from the `--listen` argument
    port = int(port)  # Convert port to an integer for Flask
    logger.info(f"Starting scraper service on {host}:{port}")
    app.run(host=host if host else "0.0.0.0", port=port)


if __name__ == '__main__':
    main()
