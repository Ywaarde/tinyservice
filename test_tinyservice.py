import unittest
import os
import json

from application import create_app, db

class TinyServiceTestCases(unittest.TestCase):

    def setUp(self):
        """Initialize app, client and in-memory db for testing."""
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client
        """Define basic data-payload for requests."""
        self.payload = {
            "url": "https://www.developers.nl",
            "shortcode": "t3st3n"
        }

    def test_shorten_code(self):
        """Test if POST request returns correct code and shortcode in body."""
        response = self.client().post('/shorten', data=self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(str, type(response.json['shortcode']))
        self.assertEqual('t3st3n', response.json['shortcode'])

    def test_shorten_code_no_code(self):
        """Test POST request without shortcode."""
        payload = {
            "url": "https://www.developers.nl"
        }
        response = self.client().post('/shorten', data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(str, type(response.json['shortcode']))

    def test_shorten_no_url(self):
        """Test POST request without url."""
        payload = {}
        response = self.client().post('/shorten', data=payload)

        self.assertEqual(response.status_code, 400)

    def test_shorten_code_in_use(self):
        """Test POST request with a shortcode that is in use"""
        self.client().post('/shorten', data=self.payload)

        response = self.client().post('/shorten', data=self.payload)

        self.assertEqual(response.status_code, 409)

    def test_shorten_invalid_code_char(self):
        """Test POST request with invalid shortcode."""
        payload = {
            "url": "https://www.developers.nl",
            "shortcode": "45&34!"
        }
        response = self.client().post('/shorten', data=payload)

        self.assertEqual(response.status_code, 412)

    def test_shorten_invalid_code_short(self):
        """Test POST request with invalid shortcode."""
        payload = {
            "url": "https://www.developers.nl",
            "shortcode": "afd45"
        }
        response = self.client().post('/shorten', data=payload)

        self.assertEqual(response.status_code, 412)

    def test_shorten_invalid_code_long(self):
        """Test POST request with invalid shortcode."""
        payload = {
            "url": "www.developers.nl",
            "shortcode": "adf45ght5"
        }
        response = self.client().post('/shorten', data=payload)

        self.assertEqual(response.status_code, 412)

    def test_return(self):
        """Test GET request with valid shortcode."""
        self.client().post('/shorten', data=self.payload)

        response = self.client().get('/t3st3n')

        self.assertEqual(response.status_code, 302)
        self.assertEqual("https://www.developers.nl", response.headers['location'])
    
    def test_return_not_found(self):
        """Test GET request with unfamiliar shortcode."""
        response = self.client().get('/404040')

        self.assertEqual(response.status_code, 404)

    def test_stats(self):
        """Test GET stats request with valid shortcode."""
        """Add to db."""
        self.client().post('/shorten', data=self.payload)
        """Hit once to update stats."""
        self.client().get('/t3st3n')
        """Get stats."""
        response = self.client().get('/t3st3n/stats')

        self.assertEqual(response.status_code, 200)
        self.assertIn('created', response.json)
        self.assertEqual(response.json['redirectCount'], 1)

    def test_stats_not_found(self):
        """Test GET stats request with unfamiliar shortcode."""
        response = self.client().get('/404040/stats')

        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            """Shut down db."""
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()