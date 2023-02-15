from django.urls import path
from .views import artist_list, artist_detail

urlpatterns = [
    path('', artist_list, name='artist_list'),
    path('artists/<slug:slug>/', artist_detail, name='artist_detail'),
]