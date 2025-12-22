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
            # Verifica se o atributo é de fato uma classe
        self.assertTrue(inspect.isclass(cls), f"{self.class_name} deve ser uma classe, não um objeto ou função.")

    def test_if_message_service_has_send_method(self) -> None:
        module = importlib.import_module(self.module_path)
        cls = getattr(module, self.class_name)
        self.assertTrue(hasattr(cls, 'send_message'), "A classe MessageService deve ter um método 'send_message'.")