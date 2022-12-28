from django.shortcuts import render, get_object_or_404

# Create your views here.
from genre.models import Genre
from medium.models import Medium
from store.models import Artwork


def store(request, mediums_slug=None):
    mediums = None
    artworks = None

    if mediums_slug != None:
        mediums = get_object_or_404(Medium, slug=mediums_slug)
        artworks = Artwork.objects.filter(medium_title=mediums, is_verified=True)
        artworks_count = artworks.count()
    else:
        artworks = Artwork.objects.all().filter(is_verified=True)
        artworks_count = artworks.count()

    context = {
        'artworks': artworks,
        'artwork_count': artworks_count
    }
    return render(request, "home.html", context)


def artwork_detail(request, mediums_slug, artwork_slug):
    try:
        single_artwork = Artwork.objects.get(medium_title__slug=mediums_slug, slug=artwork_slug)
    except Exception as e:
        raise e

    context = {
        'single_artwork': single_artwork
    }
    return render(request, "artwork_detail.html", context)