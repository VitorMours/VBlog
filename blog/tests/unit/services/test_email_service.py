from django.test import TestCase 
import inspect 
import importlib

class TestEmailService(TestCase):
    def setUp(self) -> None:
        pass
    
    
    def test_if_service_file_exists(self) -> None:
        module = importlib.import_module("blog.services.email_service")
        self.assertTrue(module)