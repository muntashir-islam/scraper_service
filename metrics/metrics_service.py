from flask import Flask, request, Response
from prometheus_client import Counter, generate_latest, start_http_server, CollectorRegistry

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


if __name__ == '__main__':
    # Run Flask app on port 9095
    app.run(host='0.0.0.0', port=9095)
