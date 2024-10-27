#!/usr/bin/env python3
from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, CollectorRegistry
import argparse

app = Flask(__name__)

custom_registry = CollectorRegistry()
# Prometheus metric to count HTTP GET requests
http_get_counter = Counter(
    'http_get', 'Counts HTTP GET requests',
    ['url', 'code'],
    registry=custom_registry
)


@app.route('/metrics')
def metrics():
    # Return the latest metrics
    return Response(generate_latest(custom_registry), mimetype='text/plain')


@app.route('/increment', methods=['POST'])
def increment_counter():
    data = request.get_json()
    url = data.get('url')
    code = data.get('code')

    if not url or not code:
        return {"error": "URL and code are required"}, 400

    # Increment the Prometheus counter with URL and status code
    http_get_counter.labels(url=url, code=code).inc()
    return {"status": "success"}, 200


def main():
    parser = argparse.ArgumentParser(description='Run the metrics service')
    parser.add_argument('--listen', type=str, default=":9095", help='Host and the port number to listen on')
    args = parser.parse_args()

    host, port = args.listen.split(':')  # Extract host and port from the `--listen` argument
    port = int(port)  # Convert port to an integer for Flask

    app.run(host=host if host else "0.0.0.0", port=port)


if __name__ == '__main__':
    # Run Flask app on port 9095
    main()
