from django.contrib import admin
from .models import PostCategory, Post, Comment, Reply

# Register your models here.
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
