import unittest

from app import app


class AdminDashboardTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_admin_login_requires_credentials(self):
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_redirects_when_not_logged_in(self):
        response = self.app.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
