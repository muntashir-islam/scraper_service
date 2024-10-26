import unittest
from flask import json
from metrics_service import app  # Replace with your actual script name if different


class MetricsServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and reset metrics data."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        # Reset metrics data before each test
        app.metrics_data = {}

    def test_increment_metric_success(self):
        """Test successful metric increment with status response."""
        response = self.client.post('/increment', json={"url": "https://google.com", "code": "200"})
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(json_data['status'], "success")

    def test_increment_metric_multiple(self):
        """Test multiple increments for the same URL and status code."""
        self.client.post('/increment', json={"url": "https://google.com", "code": "200"})
        self.client.post('/increment', json={"url": "https://google.com", "code": "200"})
        response = self.client.post('/increment', json={"url": "https://google.com", "code": "200"})

        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['status'], "success")

    def test_increment_different_codes(self):
        """Test increments for different status codes on the same URL."""
        self.client.post('/increment', json={"url": "https://google.com", "code": "200"})
        self.client.post('/increment', json={"url": "https://google.com", "code": "404"})

        response_200 = self.client.post('/increment', json={"url": "https://google.com", "code": "200"})
        response_404 = self.client.post('/increment', json={"url": "https://google.com", "code": "404"})

        json_data_200 = json.loads(response_200.data)
        json_data_404 = json.loads(response_404.data)

        self.assertEqual(json_data_200['status'], "success")
        self.assertEqual(json_data_404['status'], "success")


if __name__ == '__main__':
    unittest.main()
