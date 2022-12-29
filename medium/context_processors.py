from medium.models import Medium


def medium_links(request):
    links = Medium.objects.all()
    return dict(medium_links=links)