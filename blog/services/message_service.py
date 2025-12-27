from django.contrib import messages 
from django.http import request
from django.contrib.messages import constants
import enum


class MessageImportanceLevel(enum.Enum):
    DEBUG=10
    INFO=20
    SUCCESS=25
    WARNING=30
    ERROR=40

class MessageService:
    """
    MessageService it's a class focused in abstract the messages 
    module from the django framework, to provide a more easy way to develop and 
    use the messages in the django system to provide information and feedback for the user.
    The class it's only for organization needs, but all the work gonna be do by the methods
    of the class.
    """
    
    @classmethod
    def create_message(cls, request: request, message: str, level: MessageImportanceLevel=MessageImportanceLevel.INFO) -> None:
        """
        Method focused in to send the message for the user, and to provide some 
        type of visual feedback to the user about the actionthat it's done. This 
        function actually craete the message and 
        """
        messages.add_message(request, level.value, message)
