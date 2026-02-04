from django.contrib.auth import get_user_model
from blog.models import Visualization
User = get_user_model()

class VisualizationService:

  @staticmethod 
  def get_user_views(user: User) -> Visualization:
    visualizations = Visualization.objects.filter(user_id=user).all()
    return visualizations
  
  @staticmethod 
  def calculate_views_per_post(user: User) -> None:
    pass
  
  
  @staticmethod 
  def calculate_views_per_day(user: User) -> None:
    pass