import enum
from django.test import TestCase
import importlib
import inspect

class TestMessageService(TestCase):

    def setUp(self) -> None:
        self.module_path = "blog.services.message_service"
        self.class_name = "MessageService"

    def test_if_is_running(self) -> None:
        self.assertTrue(True)

    def test_if_message_service_file_exists(self) -> None: 
        module = importlib.import_module(self.module_path)
        self.assertIsNotNone(module)

    def test_if_message_service_class_exists(self) -> None:
        module = importlib.import_module(self.module_path)
        self.assertTrue(hasattr(module, self.class_name), f"A classe {self.class_name} não existe no módulo.")
        cls = getattr(module, self.class_name)
        self.assertTrue(inspect.isclass(cls), f"{self.class_name} deve ser uma classe, não um objeto ou função.")

    def test_if_message_service_has_create_method(self) -> None:
        module = importlib.import_module(self.module_path)
        cls = getattr(module, self.class_name)
        self.assertTrue(hasattr(cls, 'create_message'), "A classe MessageService deve ter um método 'create_message'.")
        
    def test_if_message_service_create_method_have_correct_signature(self) -> None: 
        
        module = importlib.import_module(self.module_path)
        class_ = module.MessageService
        signature = inspect.signature(class_.create_message)
        self.assertIn("message", signature.parameters.keys())                    
        self.assertIn("level", signature.parameters.keys())                    
    
    def test_if_message_service_have_importance_level_system(self) -> None:
        module = importlib.import_module(self.module_path)
        level_class_ = module.MessageImportanceLevel
        self.assertTrue(type(level_class_) is enum.EnumType)
