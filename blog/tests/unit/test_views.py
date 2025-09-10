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
    
    def test_index_view_page_header(self) -> None:
        response = self.client.get("/")
        response.content.decode("utf-8")
        self.assertIn(b'<title>VBlog</title>', response.content)
        self.assertIn(b'<a href="/" id="blog-logo" class="text-xl font-bold">VBlog</a>', response.content)
            
    def test_if_index_view_have_auth_links(self) -> None:
        response = self.client.get('/')
        response_content = response.content.decode("utf-8")
        
        self.assertIn('href="/login"', response_content)
        self.assertIn('href="/signin"', response_content)
    
    
    