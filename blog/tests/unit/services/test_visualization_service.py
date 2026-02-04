from django.test import TestCase 
import importlib 
import inspect 
from blog.models import CustomUser, Post, Visualization

class TestVisualationService(TestCase):
  def setUp(self) -> None:
    self.mock_user = CustomUser.objects.create_user(
      email="jvrezendemoura@gmail.com",
      password="123asd!"
    )
    self.mock_user.save()
    
    self.mock_post = Post(
      title = "Testando o codigo",
      content = "content",
      visibility = False,
      owner = self.mock_user
    )
    self.mock_post.save()
    
  
  def test_if_can_import_service_module(self) -> None:
    try:
      from blog.services import visualization_service
    except ImportError:
      raise ImportError("Was not possible to import visualization service")
    
  def test_if_can_import_the_service_class(self) -> None:
    try:
      from blog.services.visualization_service import VisualizationService
    except ImportError:
      raise ImportError("Was not possible to import the class")
    
  def test_if_service_have_count_visualizations_method(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService 
    self.assertTrue(hasattr(class_, "get_user_views"))
    
  def test_if_service_have_count_post_visualization_methods(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService 
    self.assertTrue(hasattr(class_, "calculate_views_per_post"))
    
  def test_if_service_have_count_visualizations_per_day_method(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService 
    self.assertTrue(hasattr(class_, "calculate_views_per_day"))
    
  def test_if_service_methods_are_all_static(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService
    calculate_user_views_method = getattr(class_, "get_user_views")
    calculate_views_per_post_method = getattr(class_, "calculate_views_per_post")
    calculate_views_per_day_method = getattr(class_, "calculate_views_per_day")
    calculate_user_views_is_static = inspect.isfunction(calculate_user_views_method)
    calculate_views_per_post_is_static = inspect.isfunction(calculate_views_per_post_method)
    calculate_views_per_day_is_static = inspect.isfunction(calculate_views_per_day_method)
    self.assertTrue(calculate_user_views_is_static)
    self.assertTrue(calculate_views_per_post_is_static)
    self.assertTrue(calculate_views_per_day_is_static)
    
  def test_if_get_user_views_method_have_correct_signature(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService
    signature = inspect.signature(class_.get_user_views)
    parameters = signature.parameters.keys()
    for parameter in parameters:
      self.assertIn(parameter, ["user"])
      
  def test_if_get_user_views_methods_returns_json(self) -> None:
    module = importlib.import_module("blog.services.visualization_service")
    class_ = module.VisualizationService
    result = class_.get_user_views(self.mock_user)
    self.assertEqual(list(result), [])
  
    view = Visualization.objects.create(
      user = self.mock_user,
      post = self.mock_post 
    )
    view.save()
    
    result = class_.get_user_views(self.mock_user)
    self.assertIsInstance(*result, Visualization)
  
    
    
  