from typing import Any, Dict, List
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from blog.models import Visualization, Post
from django.db.models import Count, Avg
User = get_user_model()

class VisualizationService:

  @staticmethod 
  def get_user_views(user: User) -> Visualization: #type: ignore
    visualizations = Visualization.objects.filter(user_id=user).all()
    return visualizations
  
  @staticmethod 
  def count_user_views(user: User) -> Visualization: #type: ignore
    visualizations = Visualization.objects.filter(post___owner=user).count()
    return visualizations
  
  @staticmethod 
  def calculate_views_per_post(user: User) -> None  : #type: ignore
    visualizations_per_post = (
    Visualization.objects
      .filter(post___owner=user)
      .values("post___title")  
      .annotate(total_views=Count('id'))
    )
    return visualizations_per_post
  
  @staticmethod
  def calculate_views_per_post_avg(user: User) -> float:
      """
      Calcula a média de visualizações por post de um usuário
      """
      avg_views = (
          Post.objects
          .filter(_owner=user)
          .annotate(total_views=Count("visualization"))
          .aggregate(avg=Avg("total_views"))
      )["avg"]
      return avg_views
      
  @staticmethod
  def count_views_today(user: User) -> int:
    """Conta visualizações do dia atual"""
    today = timezone.now().date()
    return Visualization.objects.filter(
      post___owner=user,
      created_at__date=today
    ).count()

  @staticmethod
  def calculate_views_per_day(user: User, days: int = 7) -> List[Dict[str, Any]]:
    """Calcula visualizações por dia dos últimos N dias"""
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    views_per_day = (
        Visualization.objects
        .filter(
            user=user,
            created_at__range=[start_date, end_date]
        )
        .extra({'date': "date(created_at)"})
        .values('date')
        .annotate(total_views=Count('id'))
        .order_by('date')
    )

    return list(views_per_day)