from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from blog.forms import LoginForm

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
    
    
class TestAuthViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        
    def test_if_login_view_status_code(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
    def test_if_login_view_template(self) -> None:
        self.assertTemplateUsed(self.client.get('/login'), 'login.html')
    
    def test_if_login_form_object_is_been_passed(self) -> None:
        response = self.client.get(reverse('login'))
        form = response.context.get('form')
        self.assertIsNotNone(form)
        
    def test_if_login_form_is_login_form(self) -> None:
        response = self.client.get(reverse('login'))
        form = response.context.get('form')
        self.assertIsInstance(form, LoginForm)
        
    def test_if_login_form_has_correct_fields(self) -> None:
        response = self.client.get('/login')
        form = response.context.get('form')
        self.assertTrue(form.fields, "email")
        self.assertTrue(form.fields, "password")
        
    def test_if_login_page_is_correct(self) -> None:
        response = self.client.get('/login')
        html = response.content.decode("utf-8")
        self.assertTrue(html.endswith('</html>'))
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        
    def test_if_login_page_have_form(self) -> None:
        response = self.client.get('/login')
        html = response.content.decode("utf-8")
        self.assertIn('<form>', html, "A página não contém nenhum formulário")
        self.assertIn('</form>', html, "A página não contém nenhum formulário")


    def test_if_login_is_using_csrf(self) -> None:
        response = self.client.get('/login')
        html = response.content.decode('utf-8')        
        # Verifica a presença do campo CSRF
        self.assertIn('name="csrfmiddlewaretoken"', html,
                     'Campo CSRF token não encontrado')
        
        # Verifica se é um campo hidden (geralmente é)
        self.assertIn('type="hidden"', html,
                     'CSRF token não está como campo hidden')
        
    def test_if_login_credential_input_exists(self) -> None:
        pass