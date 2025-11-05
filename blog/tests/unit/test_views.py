from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from blog.forms import LoginForm, SigninForm
from django.contrib.auth.models import User
import importlib 
import inspect


class TestCommonViews(TestCase):
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
        self.mock_user = User.objects.create_user(
                    username='testuser', 
                    email='email@email.com', 
                    password='12313asd!'
                )

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
        self.assertIn('<form', html, "A página não contém nenhum formulário")
        self.assertIn('</form>', html, "A página não contém nenhum formulário")

    def test_if_login_is_using_csrf(self) -> None:
        response = self.client.get('/login')
        html = response.content.decode('utf-8')        
        self.assertIn('name="csrfmiddlewaretoken"', html,
                     'Campo CSRF token não encontrado')
        self.assertIn('type="hidden"', html,
                     'CSRF token não está como campo hidden')

    def test_if_login_view_return_error_with_wrong_http_method(self) -> None:
        response_put = self.client.put("/login")
        response_delete = self.client.delete("/login")
        self.assertNotEqual(response_put.status_code, 200)
        self.assertNotEqual(response_delete.status_code, 200)
        self.assertEqual(response_put.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)

    def test_if_login_view_can_post_the_form_with_incorrect_data(self) -> None:
        form_data = {
            "username":"emaila@email.com",
            "password":"12313asd!"
        }
        response = self.client.post("/login", data=form_data, csrf_token=False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("login.html")

#    def test_if_login_view_can_post_the_form_correctly(self) -> None:
#        form_data = {
#            "username":'testuser', 
#            "email":'email@email.com', 
#            "password":'12313asd!'
#        }
#        response = self.client.post("/login", data=form_data, csrf_token=False)
#        self.assertEqual(response.status_code, 200)

    def test_signin_view_status_code(self) -> None:
        response = self.client.get("/signin")
        self.assertEqual(response.status_code, 200)

    def test_signin_view_status_code_reverse(self) -> None: 
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test_if_signin_page_have_form(self) -> None:
        response = self.client.get('/login')
        html = response.content.decode("utf-8")
        self.assertIn('<form', html, "A página não contém nenhum formulário")
        self.assertIn('</form>', html, "A página não contém nenhum formulário")

    def test_if_signin_is_using_csrf(self) -> None:
        response = self.client.get('/signin')
        html = response.content.decode('utf-8')        
        self.assertIn('name="csrfmiddlewaretoken"', html,
                        'Campo CSRF token não encontrado')
        self.assertIn('type="hidden"', html,
                        'CSRF token não está como campo hidden')
    
    def test_if_signin_page_is_correct(self) -> None:
        response = self.client.get('/signin')
        html = response.content.decode("utf-8")
        self.assertTrue(html.endswith('</html>'))
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_if_signin_form_is_login_form(self) -> None:
        response = self.client.get(reverse('signin'))
        form = response.context.get('form')
        self.assertIsInstance(form, SigninForm)

    def test_if_signin_view_have_post_method(self) -> None:
        response = self.client.post("/signin")
        self.assertEqual(response.status_code, 200)

    def test_if_can_reverse_the_signin_view_with_post_method(self) -> None:
        response = self.client.post(reverse("signin"))
        self.assertEqual(response.status_code, 200)

    def test_if_signin_views_is_in_views_file(self) -> None:
        module = importlib.import_module("blog.views")
        self.assertTrue(hasattr(module, "signin"))

    def test_if_signin_views_have_correct_method_params(self) -> None:
        module = importlib.import_module("blog.views")
        params = inspect.signature(module.signin)
        self.assertTrue("request" in params.parameters.keys())
    
class TestViews(TestCase):
    def setUp(self) -> None:
        pass 

    def test_if_is_running(self) -> None:
        self.assertTrue(True)

    def test_if_can_import_normal_views(self) -> None:
        pass

