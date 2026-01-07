from django.contrib.auth import get_user_model

User = get_user_model()

class AuthService:
    @staticmethod
    def check_if_email_is_registered(self) -> None:
        pass 
    
    @staticmethod 
    def check_if_account_is_active(self) -> None:
        pass
    
    @staticmethod 
    def login_user(self) -> None:
        pass
    
    @staticmethod 
    def deactivate_user(self) -> None:
        pass
    