from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from carts.models import CartItem
from carts.views import _cart_id
from genre.models import Genre
from medium.models import Medium
from store.models import Artwork, ArtworkComment, UserLikedArtwork


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
        user = request.user
        user_liked_artwork = UserLikedArtwork.objects.filter(user=user, artwork=single_artwork).exists()

        if request.method == 'POST' and request.user.is_authenticated:
            if user_liked_artwork:
                # user has already liked this artwork, so remove the like
                user_liked_artwork = UserLikedArtwork.objects.get(user=user, artwork=single_artwork)
                user_liked_artwork.delete()
            else:
                # user has not liked this artwork yet, so add the like
                user_liked_artwork = UserLikedArtwork(user=user, artwork=single_artwork)
                user_liked_artwork.save()

            # redirect back to the same artwork detail page
            return HttpResponseRedirect(reverse('artwork_detail', args=[genres_slug, artwork_slug]))

    except Artwork.DoesNotExist:
        raise Http404("Artwork does not exist")

    context = {
        'single_artwork': single_artwork,
        'in_cart': in_cart,
        'artwork_comments': artwork_comments,
        'user_liked_artwork': user_liked_artwork
    }

    return render(request, 'artwork_detail.html', context)


def search(request):
    artworks = None
    artworks_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            artworks = Artwork.objects.filter(
                Q(artwork_title__icontains=keyword) |
                Q(description__icontains=keyword)
                # | Q(artist_name__contains=keyword)
            )
            artworks_count = artworks.count()

    context = {
        'artworks': artworks,
        'artwork_count': artworks_count,
    }
    return render(request, 'home.html', context)


@login_required
def toggle_like_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)

    if request.method == 'POST':
        user = request.user
        user_liked_artwork, created = UserLikedArtwork.objects.get_or_create(user=user, artwork=artwork)

        if not created:
            user_liked_artwork.delete()

    context = {
        'user_liked_artwork': UserLikedArtwork.objects.filter(user=request.user, artwork=artwork).exists()
    }

    return JsonResponse(context)
