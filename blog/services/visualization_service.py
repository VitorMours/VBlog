import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np
from django.contrib.auth import get_user_model
User = get_user_model()

class VisualizationService:

  @staticmethod 
  def calculate_user_views(user: User) -> None:
    pass
  
  @staticmethod 
  def calculate_views_per_post(user: User) -> None:
    pass
  
  @staticmethod 
  def calculate_views_per_day(user: User) -> None:
    pass