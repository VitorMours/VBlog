from django.test import TestCase 
import inspect 
import importlib

class TestEmailService(TestCase):
    def setUp(self) -> None:
        pass
    
    def test_if_service_file_exists(self) -> None:
        module = importlib.import_module("blog.services.email_service")
        self.assertTrue(module)
        
    def test_if_can_import_the_class(self) -> None: 
        try: 
            from blog.services.email_service import EmailService
        except ImportError:
            raise ImportError("Was not possible to import the email service")
        
    def test_if_module_have_django_send_email(self) -> None:
        try: 
            from blog.services.email_service import send_mail
        except ImportError:
            raise ImportError("Was not possible to import the email service")
        
    def test_if_email_service_have_configurations_variables(self) -> None:
        