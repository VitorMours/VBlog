from django.contrib.auth.backends import BaseBackend 
from django.contrib.auth import get_user_model
from django.test import Client, TestCase 
import importlib 
import inspect 

User = get_user_model()

class TestEmailBackend(TestCase):
    def setUp(self) -> None:

        self.mock_user = User.objects.create_user(
            username="test_user",
            email="teste@teste.com",
            password="123123123"
        )

    def test_if_is_running(self) -> None:
        self.assertTrue(True)


    def test_if_can_import_backend_file(self) -> None:
        module = importlib.import_module("blog.backends")
        self.assertTrue(module)

    def test_fi_can_import_email_backend_class(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend
        self.assertTrue(class_)

    def test_if_class_is_callable(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend
        self.assertTrue(callable(class_))
        
    def test_if_class_is_base_backend_subclass(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend
        self.assertTrue(issubclass(class_, BaseBackend))

    def test_if_backend_have_authenicate_method(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend
        self.assertTrue(hasattr(class_, "authenticate"))

    def test_if_backend_have_authenticate_method_correct_paramaeters(self) -> None:
        parameters_list = ["self","request","email","password"]
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend
        signature = inspect.signature(class_.authenticate)

        for parameter in parameters_list:
            self.assertTrue(parameter in signature.parameters.keys())

    def test_if_authenticate_a_user_that_not_exists(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend()
        result = class_.authenticate(
            request = None,
            email="teste@teste.com",
            password="123123123123123"
        )
        self.assertIsNone(result)


    def test_if_can_authenticate_a_user_that_exists(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend()
        result = class_.authenticate(
            request=None,
            email="teste@teste.com",
            password="123123123"
        )
        self.assertTrue(result)

    def test_if_raise_error_without_request_in_the_authenticate_method(self) -> None:
        module = importlib.import_module("blog.backends")
        class_ = module.EmailBackend()
        with self.assertRaises(TypeError):
            result = class_.authenticate(email="teste@teste.com", password="123123123")

            
    
