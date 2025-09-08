from django.db import models
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    _title = models.CharField(max_length=100, null=False, blank=False)
    _content = models.TextField(null=False, blank=False)
    _visibility = models.BooleanField(default=False, null=False, blank=False)
    _owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
    def owner(self) -> User:
        return self._owner 

    @owner.setter 
    def owner(self, value) -> TypeError | None:
        if not isinstance(value, User):
            raise TypeError("O valor passado dentro desse campo deve ser um usuário")
        self._owner = value

    def __str__(self) -> None:
        return f"{self.title} {self.owner}: {self.visibility}"