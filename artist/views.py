from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from artist.forms import ArtistForm, AccountForm
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


def artist_edit(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    if request.method == 'POST':
        artist.artist_name = request.POST.get('artist_name')
        artist.description = request.POST.get('description')
        artist.save()
        return redirect('artist_detail', slug=slug)
    return render(request, 'artist_edit.html', {'artist': artist})

@login_required
def artist_add(request):

    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        artist_form = ArtistForm(request.POST)

        if account_form.is_valid() and artist_form.is_valid():
            account = account_form.save(commit=False)
            account.set_password(account_form.cleaned_data['password'])
            account.save()

            artist = artist_form.save(commit=False)
            artist.artist_email = account
            artist.save()

            return redirect('artist_list')
    else:
        account_form = AccountForm()
        artist_form = ArtistForm()

    context = {
        'account_form': account_form,
        'artist_form': artist_form
    }

    return render(request, 'artist_add.html', context)


def artist_delete(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    if request.method == 'POST':
        artist.delete()
        return redirect('artist_list')
    return render(request, 'artist_delete.html', {'artist': artist})



