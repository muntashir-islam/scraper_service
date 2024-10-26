#!/usr/bin/env python3
from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, generate_latest, start_http_server, CollectorRegistry
import argparse
import requests

app = Flask(__name__)

# Create a custom registry to avoid default metrics
custom_registry = CollectorRegistry()

http_get_counter = Counter (
    'http_get',
    'Number of requests performed',
    labelnames=['url', 'code'],
    registry=custom_registry  # Register counter to custom registry
)

start_http_server(9095)
@app.route('/', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')  # Get JSON data from request

    if not url:
        return jsonify({'error': 'No url provided'}), 400

    try:
        response = requests.get(url)  # Fetch HTML content of the provided URL
        # Update the Prometheus counter with the url and status code
        http_get_counter.labels(url=url, code=str(response.status_code)).inc()
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        # Increment the counter for failed requests (e.g., code 500 for exceptions)
        http_get_counter.labels(url=url, code="500").inc()
        return jsonify({'error': str(e)}), 500

    # return jsonify({'data': response.text}), 200
    return jsonify({
        "url": url,
        "status_code": response.status_code,
        "content": response.text[:200]  # Return first 200 characters of the response
    })
@app.route('/metrics')
def metrics():
    # Expose the /metrics endpoint for Prometheus to scrape
    return Response(generate_latest(custom_registry), mimetype='text/plain')  # using a custom registry to avoid default metrics


def main():
    parser = argparse.ArgumentParser(description='Run the scraper service')
    parser.add_argument('--listen', type=str, default=":8080", help='Host and the port number to listen on')
    args = parser.parse_args()

    host, port = args.listen.split(':')  # Extract host and port from the `--listen` argument
    port = int(port)  # Convert port to an integer for Flask

    app.run(host=host if host else "0.0.0.0", port=port)


if __name__ == '__main__':
    main()
