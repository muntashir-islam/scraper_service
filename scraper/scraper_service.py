#!/usr/bin/env python3
from flask import Flask, request, jsonify
import argparse
import requests
import os

app = Flask(__name__)

METRICS_SERVICE_URL = os.getenv('METRICS_SERVICE_URL', 'http://localhost:9095/increment')
@app.route('/', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')  # Get JSON data from request

    if not url:
        return jsonify({'error': 'No url provided'}), 400

    try:
        response = requests.get(url)  # Fetch HTML content of the provided URL
        status_code = str(response.status_code)
        increment_response = requests.post(METRICS_SERVICE_URL, json={"url": url, "code": status_code})
        if increment_response.status_code != 200:
            return jsonify({"error": "Failed to increment metric"}), 500

        # return jsonify({'data': response.text}), 200
        return jsonify({
            "url": url,
            "status_code": response.status_code,
            "content": response.text[:200]  # Return first 200 characters of the response
        })
    except requests.exceptions.RequestException as e:
        # Handle network issues
        return jsonify({"error": str(e)}), 500


def main():
    parser = argparse.ArgumentParser(description='Run the scraper service')
    parser.add_argument('--listen', type=str, default=":8080", help='Host and the port number to listen on')
    args = parser.parse_args()

    host, port = args.listen.split(':')  # Extract host and port from the `--listen` argument
    port = int(port)  # Convert port to an integer for Flask

    app.run(host=host if host else "0.0.0.0", port=port)


if __name__ == '__main__':
    main()
