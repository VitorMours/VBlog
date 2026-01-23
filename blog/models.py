from django.db import models
import __future__
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
import uuid
import textwrap

# render markdown to html safely
try:
    import markdown as _markdown
    import bleach as _bleach
except Exception:
    _markdown = None
    _bleach = None

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
        """Renderiza o Markdown do `content` para HTML sanitizado.

        Usa `markdown` + `bleach` quando disponíveis. Se as libs
        não estiverem instaladas, retorna o texto cru escapado em <pre>.
        Também remove indentação acidental com `textwrap.dedent`.
        """
        raw = self._content or ''
        # remove indentation acidental (ex.: copiar/colar)
        dedented = textwrap.dedent(raw)

        if _markdown and _bleach:
            # extensões que aproximam GFM e preservam listas/quebras
            html = _markdown.markdown(dedented, extensions=["extra", "sane_lists", "codehilite"], output_format='html5')

            # permitir tags comuns geradas por markdown
            allowed_tags = [
                'a','abbr','acronym','b','blockquote','code','em','i','li','ol','pre','strong','ul',
                'p','h1','h2','h3','h4','h5','h6','br','hr','img','table','thead','tbody','tr','th','td'
            ]
            allowed_attrs = {
                '*': ['class', 'id'],
                'a': ['href', 'title', 'rel', 'target'],
                'img': ['src', 'alt', 'title'],
                'th': ['colspan', 'rowspan'],
                'td': ['colspan', 'rowspan']
            }

            clean = _bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
            # permitir links seguros
            clean = _bleach.linkify(clean)
            return clean

        # fallback simples: escapar dentro de <pre>
        import html as _html
        return f"<pre>{_html.escape(dedented)}</pre>"

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

class RankingVotes(models.Model):
    _id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4, editable=False)
    origin_post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    user_id= models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    vote_value = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    