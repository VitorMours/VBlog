from django.test import TestCase
import importlib 
import inspect 


class TestAuthService(TestCase):
    def setUp(self) -> None:
        pass
    
    def test_if_can_import_file(self) -> None:
        try:
            import blog.services.auth_service
        except ImportError:
            raise ImportError("Was not possible to import the auth service")
        
        
    def test_if_auth_service_class_exists(self) -> None:
        try:
            module = importlib.import_module("blog.services.auth_service")
            class_ = module.AuthService
            self.assertTrue(inspect.isclass(class_))
            
        except ImportError:
            raise ImportError("Was not possible to import he auth service")
        except AttributeError:
            raise AttributeError("The class that it's accessed not exist in the file")

    def test_if_auth_service_class_have_the_method_to_check_email_in_database(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService
        self.assertTrue(hasattr(class_, "check_if_email_is_registered"))

    def test_if_auth_service_class_have_the_method_to_check_if_account_its_activate(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService
        self.assertTrue(hasattr(class_, "check_if_account_is_active"))
        
    def test_if_auth_service_have_login_user_method(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService
        self.assertTrue(hasattr(class_, "login_user"))
        
    def test_if_auth_service_have_deactivate_user_method(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        self.assertTrue(hasattr(class_, "deactivate_user"))
       
    
       
     
        
        
        