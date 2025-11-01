from django.test import TestCase 
from blog.models import Post
from django.contrib.auth.models import User

class TestPostModel(TestCase):
    def setUp(self) -> None:
        mock_user = User("vitor moura","vitormoura@gmail.com","password")

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
    def test_if_user_field_exists_in_model(self) -> None:
        self.assertTrue(hasattr(Post, "user"))
        
    def test_name_equals_emoji(self) -> None: #TODO: Verificar a remoção de emojis como possibilidade de serem passados dentro do banco de dados
        user = User(username="😊")
        self.assertEqual(user.username, "😊")