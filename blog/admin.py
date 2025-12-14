from django.contrib import admin
from blog.models import CustomUser, Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass