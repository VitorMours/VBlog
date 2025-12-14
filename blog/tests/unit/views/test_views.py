from django.test import TestCase, Client
from django.urls import reverse
import importlib
from django.contrib.auth import get_user_model 
from inspect import signature

User = get_user_model()

class TestRecentView(TestCase):
    def setUp(self) -> None: 
        self.client = Client()

    def test_if_recents_view_exists(self):
        module = importlib.import_module("blog.views")
        self.assertTrue(hasattr(module, "recents"))
        
    def test_if_recent_views_have_correct_parameters(self):
        module = importlib.import_module("blog.views")
        recents_view = getattr(module, "recents", None)
        self.assertIsNotNone(recents_view, "The 'recents' view does not exist.")
        params = signature(recents_view).parameters
        self.assertIn("request", params, "The 'recents' view must have 'request' as a parameter.")  
        
    def test_recents_view_is_in_urls(self):
        url_module = importlib.import_module("blog.urls")
        url_patterns = getattr(url_module, "urlpatterns", [])
        urls_name = [url.name for url in url_patterns]
        self.assertIn("recents", urls_name, "The 'recents' view is not mapped in the URL patterns.")        
    
    def test_recents_view_requires_login(self):
        response = self.client.get(reverse("recents"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url, "The 'recents' view does not redirect to login for unauthenticated users.")



class TestCreatePostView(TestCase):
    
    def setUp(self) -> None: 
        self.client = Client()
        
    def test_if_create_post_function_exists(self) -> None:
        module = importlib.import_module("blog.views")
        self.assertTrue(hasattr(module, "create_post"))
        
    def test_if_create_post_view_have_url_registered(self) -> None:
        response = self.client.get(reverse("create_post"))
        self.assertTrue(response)
        
    def test_if_create_post_view_have_correct_signature(self) -> None: 
        module = importlib.import_module("blog.views")
        signature_ = signature(module.create_post).parameters
        self.assertIn("request", signature_)    
    
    # TODO: Corrigir
    # def test_if_create_post_view_use_correct_template(self) -> None:
    #     response = self.client.get("/create_post")
    #     self.assertTemplateUsed(response, "create_post.html")
    
    
    
class TestRelevantView(TestCase):
    
    def setUp(self) -> None: 
        self.client = Client()
        
    def test_if_relevant_view_exists(self) -> None:
        module = importlib.import_module("blog.views")
        self.assertTrue(hasattr(module, "relevant"))
        
    def test_if_relevant_view_have_url_registered(self) -> None:
        response = self.client.get(reverse("relevant"))
        self.assertTrue(response)
        
    def test_if_relevant_view_have_correct_signature(self) -> None: 
        module = importlib.import_module("blog.views")
        signature_ = signature(module.relevant).parameters
        self.assertIn("request", signature_)