from django.urls import path

from store import views

urlpatterns = [
    path('genres/<slug:genres_slug>', views.store, name='artwork_by_genres'),
    path('mediums/<slug:mediums_slug>', views.store_medium, name='artwork_by_mediums'),
    path('search/', views.search, name='search'),
    path('<slug:genres_slug>/<slug:artwork_slug>/', views.artwork_detail, name='artwork_detail'),
    path('<slug:genres_slug>/<slug:artwork_slug>/place_bid/', views.place_bid, name='place_bid'),
]