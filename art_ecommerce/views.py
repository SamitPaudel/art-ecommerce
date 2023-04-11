from django.shortcuts import render

from store.models import Artwork


def home(request):
    artworks = Artwork.objects.all().filter(isApproved=True, isAvailable=True)
    artworks_count = artworks.count()
    context = {
        'artworks': artworks,
        'artworks_count': artworks_count
    }
    return render(request, "home.html", context)
