import unittest
from uuid import uuid4

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_renders(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ade & Ade', response.data)

    def test_contact_endpoint_saves_message(self):
        response = self.app.post('/api/contact', data={
            'name': 'Ada',
            'phone': '08012345678',
            'email': 'ada@example.com',
            'subject': 'Quote',
            'message': 'Need a solar quote'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Message received', response.get_data(as_text=True))

    def test_contact_endpoint_accepts_json_payload(self):
        response = self.app.post('/api/contact', json={
            'name': 'Grace',
            'phone': '08023456789',
            'email': 'grace@example.com',
            'subject': 'Solar',
            'message': 'Need installation advice'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Message received', response.get_data(as_text=True))

    def test_subscribe_endpoint_saves_email(self):
        unique_email = f'{uuid4().hex[:8]}@example.com'
        response = self.app.post('/api/subscribe', data={'email': unique_email})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Thank you', response.get_data(as_text=True))

    def test_malformed_payload_returns_validation_error(self):
        response = self.app.post('/api/contact', json=['invalid', 'payload'])
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please fill in all fields', response.get_data(as_text=True))

    def test_not_found_page_renders_custom_error_template(self):
        response = self.app.get('/does-not-exist')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page not found', response.get_data(as_text=True))

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ok', response.get_data(as_text=True).lower())


if __name__ == '__main__':
    unittest.main()
