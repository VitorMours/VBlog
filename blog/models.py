from django.db import models
import __future__
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
import uuid
import markdown

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
        return user

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
    username = models.CharField(unique=False)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"

class Post(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4, editable=False)
    _title = models.CharField(max_length=100, null=False, blank=False)
    # _url = models.SlugField(unique=True, editable=False)
    _content = models.TextField(null=False, blank=False)
    _visibility = models.BooleanField(default=False, null=False, blank=False)
    _owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    _created_at = models.DateTimeField(auto_now_add=True)
    _updated_at = models.DateTimeField(auto_now=True)
    _status = models.IntegerField(null=False, default=0)
    
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
    def content_html(self) -> str:
        """Renderiza o Markdown para HTML de forma limpa."""
        text = self.content
        html = markdown.markdown(text, extensions=[
            'extra',          # Tabelas, definições, etc
            'codehilite',     # Syntax highlighting
            'toc',            # Table of Contents
            'sane_lists',     # Listas mais lógicas
            'nl2br',          # Quebras de linha viram <br>
            'fenced_code',    # Blocos de código com ```
            'tables',         # Suporte a tabelas Markdown
            'smarty',         # Aspas inteligentes, travessões
            'legacy_em',      # Suporte a _itálico_ e __negrito__
            'md_in_html',     # Markdown dentro de tags HTML
        ])
        
        return html

    @property
    def owner(self) -> CustomUser:
        return self._owner 

    @owner.setter 
    def owner(self, value) -> TypeError | None:
        if not isinstance(value, CustomUser):
            raise TypeError("O valor passado dentro desse campo deve ser um usuário")
        self._owner = value

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at
    
    @created_at.setter
    def created_at(self):
        return self._created_at
    
    @updated_at.setter
    def updated_at(self):
        return self._updated_at

    @property 
    def status(self) -> int:
        return self._status 
    
    @status.setter 
    def status(self, value: int) -> None:
        self._status = value
    
    def __str__(self) -> None:
        return f"{self.title} {self.owner}: {self.visibility}"

class Votes(models.Model):
    _id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4, editable=False)
    origin_post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    vote_value = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"{self.origin_post}: {self.vote_value}"
    
class Visualization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, blank=False, null=False, editable=False)
    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    