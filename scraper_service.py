#!/usr/bin/env python3
import argparse

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')  # Get JSON data from request

    if not url:
        return jsonify({'error': 'No url provided'}), 400

    try:
        response = requests.get(url)  # Fetch HTML content of the provided URL
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'data': response.text}), 200


def main():
    parser = argparse.ArgumentParser(description='Run the scraper service')
    parser.add_argument('--listen', type=str, default=":8080", help='Host and the port number to listen on')
    args = parser.parse_args()

    host, port = args.listen.split(':')  # Extract host and port from the `--listen` argument
    port = int(port)  # Convert port to an integer for Flask

    app.run(host=host if host else "0.0.0.0", port=port)


if __name__ == '__main__':
    main()
