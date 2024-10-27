import unittest
from flask import json

from scraper_service import app  # Adjust the import based on your file structure


class SimpleScraperTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_scrape_valid_url(self):
        """Test scraping a valid URL."""
        response = self.client.post('/', json={"url": "https://google.com"})
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK response
        json_data = json.loads(response.data)
        self.assertIn('url', json_data)  # Check if 'url' is in the response
        self.assertEqual(json_data['url'], "https://google.com")  # Validate the URL

    def test_scrape_no_url_provided(self):
        """Test when no URL is provided."""
        response = self.client.post('/', json={})
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'No url provided')

    def test_scrape_invalid_url_format(self):
        """Test with an invalid URL format."""
        response = self.client.post('/', json={"url": "not-a-valid-url"})
        self.assertEqual(response.status_code, 500)
        json_data = json.loads(response.data)
        self.assertIn('error', json_data)


if __name__ == '__main__':
    unittest.main()
