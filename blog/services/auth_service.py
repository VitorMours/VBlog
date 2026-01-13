from django.contrib.auth import get_user_model
User = get_user_model()

class AuthService:
    @staticmethod
    def check_if_email_is_registered(email: str) -> bool:
        return User.objects.filter(email=email).exists()
    
    @staticmethod 
    def check_if_account_is_active(email: str) -> bool | ValueError: # type: ignore
        try:
            return User.objects.get(email=email).is_active
        except ValueError:
            raise ValueError("...")    
        except User.DoesNotExist:
            return ValueError("...")
    
    @staticmethod 
    def login_user() -> None:
        pass
    
    @staticmethod 
    def deactivate_user() -> None:
        pass
    