from django.contrib import admin
from blog.models import CustomUser, Post, Visualization, Votes

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Visualization)
class VisualizationAdmin(admin.ModelAdmin):
    pass 

@admin.register(Votes)
class VotesAdmin(admin.ModelAdmin):
    pass