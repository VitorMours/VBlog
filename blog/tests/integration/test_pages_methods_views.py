from django.test import TestCase, Client 
import importlib

class TestAuthViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_if_is_running(self) -> None:
        self.assertTrue(True)

    def test_if_can_import_urls(self) -> None:
        urls = importlib.import_module("blog.urls")
        self.assertTrue(hasattr(urls, "urlpatterns"))

    
#    def test_if_the_dashboard_view_use_correct_template_when_can_login(self) -> None:
#        response = self.client.get("/dashboard")
#        self.assertEqual(response.status_code, 302)
#        self.assertTemplateUsed(response, "dashboard.html")