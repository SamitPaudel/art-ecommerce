from django.urls import path
from .views import artist_list, artist_detail, artist_edit, artist_delete, artist_add

urlpatterns = [
    path('', artist_list, name='artist_list'),
    path('artists/add_artist/', artist_add, name='artist_add'),
    path('artists/<slug:slug>/', artist_detail, name='artist_detail'),
    path('artists/<slug:slug>/edit/', artist_edit, name='artist_edit'),
    path('artists/<slug:slug>/delete/', artist_delete, name='artist_delete'),
]
