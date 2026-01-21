from django.test import TestCase
from django.contrib.auth import get_user_model
import importlib 
import inspect 


class TestAuthService(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            email="teste@teste.com",
            first_name="testando codigo", 
            last_name=" mockson da sivla",
            password="teste123!",
        )
        
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
       
    def test_if_check_email_method_is_static(self) -> None:
        function_signature = ("email")
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        method = class_.__dict__.get("check_if_email_is_registered")
        self.assertIsInstance(method, staticmethod)
        
        signature = inspect.signature(method.__func__)
        parameters = list(signature.parameters.keys())
        self.assertEqual(parameters, [function_signature])
              
    def test_if_can_check_email_method(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        result = class_.check_if_email_is_registered(self.user.email)
        self.assertTrue(result)

    def test_if_check_email_method_return_false_for_unregistered_email(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        result = class_.check_if_email_is_registered("doesnot@exists.com")
        self.assertFalse(result)
        
    def test_if_check_account_is_Active_method_is_static(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        method = class_.__dict__.get("check_if_account_is_active")
        self.assertIsInstance(method, staticmethod)
        
    def test_if_check_account_is_active_method_have_parameters(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService
        method = class_.__dict__.get("check_if_account_is_active")
        signature = inspect.signature(method.__func__)
        parameters = list(signature.parameters.keys())
        self.assertEqual(parameters, ["email"])    
    
    def test_if_can_check_if_account_is_active(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        result = class_.check_if_account_is_active(self.user.email)
        self.assertTrue(result)
        
        
    def test_if_deactivate_user_method_is_static(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        method = class_.__dict__.get("deactivate_user")
        self.assertIsInstance(method, staticmethod)

    def test_if_deactivate_user_have_correct_parameters(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        method = inspect.signature(class_.deactivate_user)
        parameters = list(method.parameters.keys())
        self.assertEqual(parameters, ["user"])
        
    def test_if_deactivate_user_works(self) -> None:
        module = importlib.import_module("blog.services.auth_service")
        class_ = module.AuthService 
        class_.deactivate_user(self.user)
        assert self.user.is_active == False
        
    