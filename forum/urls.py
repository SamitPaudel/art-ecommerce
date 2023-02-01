from django.urls import path

from forum import views
from forum.views import detail, posts

urlpatterns = [
    path('', views.home, name='forum'),
    path('detail/', detail, name='detail'),
    path('posts/', posts, name='posts'),
]