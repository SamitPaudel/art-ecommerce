from django.urls import path

from forum import views
from forum.views import detail, posts, create_post, search_result

urlpatterns = [
    path('', views.home, name='forum'),
    path('detail/<slug>/', detail, name='detail'),
    path('posts/<slug>/', posts, name='posts'),
    path('create_post', create_post, name='create_post'),
    path('search', search_result, name='search_result'),
]