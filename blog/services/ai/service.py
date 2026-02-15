from blog.services.ai.gemini_client import GeminiClient
from blog.services.ai.prompts import BlogPrompts

class GeminiService:

  MODEL = "gemini-2.5-flash-lite"

  @classmethod
  def summarize_post(cls, content: str) -> str:
    client = GeminiClient.get_client()

    response = client.models.generate_content(
      model=cls.MODEL,
      contents=BlogPrompts.summarize(content)
    )

    return response.text

  @classmethod
  def improve_post(cls, content: str) -> str:
    client = GeminiClient.get_client()

    response = client.models.generate_content(
      model=cls.MODEL,
      contents=BlogPrompts.improve(content)
    )

    return response.text