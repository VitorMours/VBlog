from django.test import TestCase 
from blog.models import Post
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.contrib.auth import get_user_model
import importlib 
import inspect

User = get_user_model()

class TestCustomUserModel(TestCase):
    def setUp(self) -> None:
        pass 
    
    def test_if_is_running(self) -> None:
        self.assertTrue(True)

    def test_if_class_custom_user_exists(self) -> None:
        module = importlib.import_module("blog.models")
        self.assertTrue(hasattr(module, "CustomUser"))

    def test_if_class_is_abstract_user_sub_class(self) -> None:
        module = importlib.import_module("blog.models")
        class_ = module.CustomUser
        self.assertTrue(issubclass(class_, AbstractUser))

    def test_if_custom_user_class_have_manager(self) -> None:
        module = importlib.import_module("blog.models")
        class_ = module.CustomUser
        self.assertTrue(hasattr(class_, "objects"))

    def test_if_custom_user_objects_is_a_manager(self) -> None:
        module = importlib.import_module("blog.models")
        class_ = module.CustomUser
        self.assertTrue(isinstance(class_.objects, BaseUserManager))


class TestPostModel(TestCase):
    def setUp(self) -> None:
        mock_user = User(first_name="vitor moura",email="vitormoura@gmail.com",password="password")

        self.mock_post = Post(
            title = "New post",
            content="Creating a post to test the test suit",
            visibility = False,
            owner = mock_user
        )

    def test_if_its_been_called(self) -> None:
        self.assertTrue(True)

    def test_if_post_model_exists(self) -> None:
        try:
            from blog.models import Post
            self.assertTrue(True, "Import Successful")
        except ImportError as e:
            self.fail(f"Import error from {e}")
    
    def test_post_model_have_title_field(self) -> None:
        self.assertTrue(hasattr(Post, "title"))
    
    def test_post_model_have_content_field(self) -> None:
        self.assertTrue(hasattr(Post, "content"))
    
    def test_post_model_have_owner_field(self) -> None:
        self.assertTrue(hasattr(Post, "owner"))
    
    def test_post_model_have_visibility_field(self) -> None:
        self.assertTrue(hasattr(Post, "visibility"))

    def test_post_model_have_id_field(self) -> None:
        self.assertTrue(hasattr(Post, "id"))

    def test_if_post_model_has_string_representation(self) -> None:
        self.assertEqual(str(self.mock_post), f"{self.mock_post.title} {self.mock_post.owner}: {self.mock_post.visibility}")   
    
    def test_create_post_with_wrong_type_in_visibility_field(self) -> None:
        with self.assertRaises(TypeError):
            post = Post(
                visibility=123
            )
    
    def test_create_post_with_wrong_type_in_title_field(self) -> None:
        with self.assertRaises(TypeError):
            post = Post(
                title=123
            )

    def test_create_post_with_wrong_type_in_content_field(self) -> None:
        with self.assertRaises(TypeError):
            post = Post(
                content=123
            )

    def test_create_post_with_wrong_type_in_owner_field(self) -> None:
        with self.assertRaises(TypeError):
            post = Post(
                owner=123
            )
        
    def test_name_equals_emoji(self) -> None:
        user = User(username="😊")
        self.assertEqual(user.username, "😊")