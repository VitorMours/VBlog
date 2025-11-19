from django.test import TestCase, Client
from django.urls import reverse

class TestUrls(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        
    def test_index_url_resolves(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_post_method_not_allowed(self) -> None:
        response_post = self.client.post(reverse('index'))
        response_put = self.client.put(reverse('index'))
        response_delete = self.client.delete(reverse('index'))
        self.assertEqual(response_post.status_code, 405)
        self.assertEqual(response_put.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)

    def test_index_url_name_resolves(self) -> None:
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_url_template(self) -> None:
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')

    def test_response_headers(self) -> None:
        response = self.client.get(reverse('index'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        
class TestAuthUrls(TestCase):
    
    def setUp(self) -> None: 
        self.client = Client()
        self.signin_response = self.client.get('/signin')
        self.login_response = self.client.get('/login')
    
    def test_login_url_name_resolves(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
    def test_login_url_resolves(self) -> None:
        self.assertEqual(self.login_response.status_code, 200)
        
    def test_login_url_template(self) -> None:
        self.assertTemplateUsed(self.login_response, "login.html")
        
    def test_login_url_headers(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.headers['Content-Type'], 'text/html; charset=utf-8')
        
    def test_login_view_not_allowed_methods(self) -> None:
        response_put = self.client.put(reverse('login'))
        response_delete = self.client.delete(reverse('login'))
        self.assertEqual(response_put.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)
        
    def test_signin_url_name_resolves(self) -> None:
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test_signin_url_resolves(self) -> None:
        self.assertEqual(self.signin_response.status_code, 200)
        
    def test_signin_url_template(self) -> None:
        self.assertTemplateUsed(self.signin_response, 'signin.html')
        
    def test_signin_url_headers(self) -> None:
        self.assertEqual(self.signin_response.headers['Content-Type'], 'text/html; charset=utf-8')
        
    def test_singin_view_not_allowed_methods(self) -> None:
        response_put = self.client.put(reverse('signin'))
        response_delete = self.client.delete(reverse('signin'))
        self.assertEqual(response_put.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)

    def test_if_logout_route_resolves(self) -> None:
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 200)