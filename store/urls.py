from django.urls import path

from store import views

urlpatterns = [
    path('<slug:genres_slug>', views.store, name='artwork_by_genres'),
    path('<slug:mediums_slug>', views.store, name='artwork_by_mediums'),
    path('<slug:genres_slug>/<slug:artwork_slug>/', views.artwork_detail, name='artwork_detail')
]