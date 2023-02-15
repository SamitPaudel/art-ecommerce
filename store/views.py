from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from artist.models import Artist
from carts.models import CartItem
from carts.views import _cart_id
from genre.models import Genre
from medium.models import Medium
from store.models import Artwork, ArtworkComment


def store(request, genres_slug=None):
    genres = None
    artworks = None

    context = {}
    if genres_slug is not None:
        genres = get_object_or_404(Genre, slug=genres_slug)
        artworks = Artwork.objects.filter(genre=genres, is_verified=True)
        paginator = Paginator(artworks, 9)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()
    else:
        artworks = Artwork.objects.all().order_by('id')
        paginator = Paginator(artworks, 9)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()

    context = {
            'artworks': paged_artworks,
            'artworks_count': artworks_count
    }

    return render(request, 'home.html', context)


def store_medium(request, mediums_slug=None):
    mediums = None
    artworks = None

    if mediums_slug is not None:
        mediums = get_object_or_404(Medium, slug=mediums_slug)
        artworks = Artwork.objects.filter(medium_title=mediums, is_verified=True)
        paginator = Paginator(artworks, 1)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()
    else:
        artworks = Artwork.objects.all().order_by('artwork_title')
        paginator = Paginator(artworks, 1)
        page = request.GET.get('page')
        paged_artworks = paginator.get_page(page)
        artworks_count = artworks.count()

    context = {
        'artworks': paged_artworks,
        'artworks_count': artworks_count
    }

    return render(request, 'home.html', context)



def artwork_detail(request, genres_slug, artwork_slug):
    try:
        single_artwork = Artwork.objects.get(genre__slug=genres_slug, slug=artwork_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), artwork=single_artwork).exists()
        artwork_comments = ArtworkComment.objects.filter(artwork=single_artwork)

        if request.method == 'POST' and request.user.is_authenticated:
            comment_content = request.POST.get('comment_content')
            user = request.user
            artwork_comment = ArtworkComment(user=user, artwork=single_artwork, content=comment_content)
            artwork_comment.save()

    except Exception as e:
        raise e

    context = {
        'single_artwork': single_artwork,
        'in_cart': in_cart,
        'artwork_comments': artwork_comments,
    }

    return render(request, 'artwork_detail.html', context)


def price_selection(request):
    artwork = Artwork.objects.all()

    # Get minimum and maximum prices from request parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter artwork by price range
    if min_price and max_price:
        artwork = artwork.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'artwork': artwork,
    }
    return render(request, 'home.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            artworks = Artwork.objects.filter(
                Q(artwork_title__icontains=keyword) |
                Q(description__icontains=keyword)
                #| Q(artist_name__contains=keyword)
            )
            artworks_count = artworks.count()

    context = {
        'artworks': artworks,
        'artwork_count': artworks_count,
    }
    return render(request, 'home.html', context)


