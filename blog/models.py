from django.db import models
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    visibility = models.BooleanField(default=False, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> None:
        return f"{self.title} {self.owner}: {self.visibility}"