from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import Http404
from django.shortcuts import render, redirect

from artist.models import Artist
from store.models import Artwork


def artist_list(request):
    artists = Artist.objects.all().order_by('artist_name')
    context = {
        'artists': artists,
    }
    return render(request, 'artist_list.html', context)

def artist_detail(request, slug):
    try:
        artist = Artist.objects.get(slug=slug)
        artwork_list = Artwork.objects.filter(artist_name=artist)
    except Artist.DoesNotExist:
        raise Http404("Artist does not exist")

    context = {
        'artist': artist,
        'artwork_list': artwork_list
    }
    return render(request, 'artist_detail.html', context)



