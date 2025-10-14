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

    