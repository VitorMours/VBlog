from django.db import models
import __future__
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields) -> "CustomUser": # type: ignore
        if not email:
            raise ValueError("The email field must be set")
        elif not password:
            raise ValueError("The password field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, email, password, **extra_fields) -> "CustomUser": # type: ignore
        if not email or not password:
            raise ValueError("The email field must be set")
        
        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager() # type: ignore

    REQUIRED_FIELDS = ["email","password"]
    USERNAME_FIELDS = ["email"]


class Post(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    _title = models.CharField(max_length=100, null=False, blank=False)
    _content = models.TextField(null=False, blank=False)
    _visibility = models.BooleanField(default=False, null=False, blank=False)
    _owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def visibility(self) -> bool:
        return self._visibility

    @visibility.setter 
    def visibility(self, value) -> None | TypeError:
        if not isinstance(value, bool):
            raise TypeError("O tipo primitivo desse campo deve ser booleano")
        self._visibility = value

    @property 
    def title(self) -> str:
        return self._title 

    @title.setter 
    def title(self, value) -> None | TypeError:
        if not isinstance(value, str):
            raise TypeError("O valor passado deve ser do tipo primitivo string")
        self._title = value

    @property 
    def content(self) -> str: 
        return self._content 

    @content.setter 
    def content(self, value) -> None | TypeError: 
        if not isinstance(value, str):
            raise TypeError("O valor passado deve ser do tipo primitivo string")
        self._content = value

    @property
    def owner(self) -> CustomUser:
        return self._owner 

    @owner.setter 
    def owner(self, value) -> TypeError | None:
        if not isinstance(value, CustomUser):
            raise TypeError("O valor passado dentro desse campo deve ser um usuário")
        self._owner = value

    def __str__(self) -> None:
        return f"{self.title} {self.owner}: {self.visibility}"

