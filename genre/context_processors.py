from genre.models import Genre


def genre_links(request):
    links = Genre.objects.all()
    return dict(links=links)