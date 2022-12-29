from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from carts.models import CartItem
from carts.views import _cart_id
from genre.models import Genre
from medium.models import Medium
from store.models import Artwork


def store(request, mediums_slug=None, genres_slug=None):
    global paged_artworks
    # mediums = None
    artworks = None

    # if mediums_slug != None:
    #     mediums = get_object_or_404(Medium, slug=mediums_slug)
    #     artworks = Artwork.objects.filter(medium_title=mediums, is_verified=True)
    #     artworks_count = artworks.count()
    # else:
    #     artworks = Artwork.objects.all().filter(is_verified=True)
    #     artworks_count = artworks.count()

    if genres_slug != None:
        genres = get_object_or_404(Genre, slug=genres_slug)
        artworks = Artwork.objects.filter(genre=genres, is_verified=True)
        paginator = Paginator(artworks, 3)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()
    else:
        artworks = Artwork.objects.all().filter(is_verified=True)
        paginator = Paginator(artworks, 3)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()

    context = {
        'artworks': paged_artworks,
        'artwork_count': artworks_count,
    }
    return render(request, "home.html", context)


def artwork_detail(request, genres_slug, artwork_slug):
    try:
        single_artwork = Artwork.objects.get(genre__slug=genres_slug, slug=artwork_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), artwork=single_artwork).exists()

    except Exception as e:
        raise e

    context = {
        'single_artwork': single_artwork,
        'in_cart': in_cart,
    }

    return render(request, 'artwork_detail.html', context)