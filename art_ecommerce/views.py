from django.shortcuts import render

from store.models import Artwork


def home(request):
    artworks = Artwork.objects.all().filter(isApproved=True)
    context = {
        'artworks': artworks
    }
    return render(request, "home.html", context)
