from django.core.mail import send_mail

class EmailService:
  """
  Class Focused in sending the user emails of any type in case of necessecity 
  of in case of solicitation of specific services of the application.
  """


  @staticmethod 
  def send() -> None:
    """
    Abstraction of the send mail method from the django core framework part.
    """
    pass