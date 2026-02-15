from google import genai 
from django.conf import settings 


class GeminiClient:
  _client = None 
  
  @classmethod
  def get_client(cls):
    if cls._client is None:
      cls._client = genai.Client(
          api_key=settings.GEMINI_API_KEY
      )
    return cls._client