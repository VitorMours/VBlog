
from django.test import TestCase

class TestUrls(TestCase):
    def test_index_url_resolves(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    