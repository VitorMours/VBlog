from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseNotAllowed

class TestViews(TestCase):
    def setUp(self) -> None: 
        self.client = Client()
    def test_index_view_status_code(self) -> None:
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200) 
        
    def test_index_view_template(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
        
    def test_index_view_page_header(self) -> None:
        response = self.client.get('/')
        response.content.decode("utf-8")
        self.assertIn(b'<title>VBlog</title>', response.content)
    
    def test_index_view_post_method_not_allowed(self) -> None:
        response = self.client.post(reverse('index'))
        self.assertEqual(response.status_code, 405)